import glob
import logging.config
import os

import numpy as np
import pandas as pd
from pynwb import NWBFile, ProcessingModule
from pynwb.behavior import Position
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile
from rec_to_nwb.processing.exceptions.invalid_metadata_exception import \
    InvalidMetadataException
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from scipy.ndimage import label
from scipy.stats import linregress

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=os.path.join(str(path), os.pardir, os.pardir,
                       os.pardir, 'logging.conf'),
    disable_existing_loggers=False)
logger = logging.getLogger(__name__)

NANOSECONDS_PER_SECOND = 1e9


class PositionOriginator:

    @beartype
    def __init__(self, datasets: list, metadata: dict, dataset_names: list):
        self.datasets = datasets
        self.dataset_names = dataset_names
        self.metadata = metadata
        self.pm_creator = ProcessingModule(
            'behavior', 'Contains all behavior-related data')

    @beartype
    def make(self, nwb_content: NWBFile):
        position = Position(name='position')
        cameras_ids = get_cameras_ids(self.dataset_names, self.metadata)
        meters_per_pixels = get_meters_per_pixels(cameras_ids, self.metadata)
        position_tracking_paths = []
        for dataset in self.datasets:
            for pos_file in dataset.get_all_data_from_dataset('pos'):
                if pos_file.endswith('.pos_online.dat'):
                    position_tracking_paths.append(
                        os.path.join(dataset.get_data_path_from_dataset('pos'),
                                     pos_file))
        first_timestamps = []
        for series_id, (conversion, position_tracking_path) in enumerate(
                zip(meters_per_pixels, position_tracking_paths)):
            position_df = self.get_position_with_corrected_timestamps(
                position_tracking_path)
            position.create_spatial_series(
                name=f'series_{series_id}',
                description=', '.join(position_df.columns.tolist()),
                data=np.asarray(position_df),
                conversion=conversion,
                reference_frame='Upper left corner of video frame',
                timestamps=np.asarray(position_df.index),
            )
            first_timestamps.append(position_df.index[0])

        # check if timestamps are in order
        first_timestamps = np.asarray(first_timestamps)
        assert np.all(first_timestamps[:-1] < first_timestamps[1:])

        logger.info('Position: Injecting into Processing Module')
        nwb_content.processing['behavior'].add(position)

    @staticmethod
    def get_position_with_corrected_timestamps(position_tracking_path):
        logger.info(os.path.split(position_tracking_path)[-1])

        position_tracking = pd.DataFrame(
            readTrodesExtractedDataFile(position_tracking_path)['data']
        ).set_index('time')

        video_info = get_video_info(position_tracking_path)

        # On AVT cameras, HWFrame counts wraps to 0 above this value.
        AVT_camHWframeCount_wrapval = 65535
        video_info['HWframeCount'] = np.unwrap(
            video_info['HWframeCount'], period=AVT_camHWframeCount_wrapval)

        dio_camera_ticks = find_camera_dio_channel(
            position_tracking_path, video_info)
        mcu_neural_timestamps = get_mcu_neural_timestamps(
            position_tracking_path)

        dio_systime = np.asarray(
            mcu_neural_timestamps.loc[dio_camera_ticks])
        pause_mid_time = find_acquisition_timing_pause(dio_systime)
        frame_rate_from_dio = get_framerate(
            dio_systime[dio_systime > pause_mid_time])
        logger.info('Camera frame rate estimated from DIO camera ticks:'
                    f' {frame_rate_from_dio:0.1f} cm/s')

        # Match the camera frames to the position tracking
        # Number of video frames can be different from online tracking because
        # online tracking can be started or stopped before video is stopped.
        # Additionally, for offline tracking, frames can be skipped if the
        # frame is labeled as bad.
        video_info = video_info.loc[position_tracking.index.unique()]
        frame_count = np.asarray(video_info.HWframeCount)
        ptp_systime = np.asarray(video_info.HWTimestamp)

        ptp_enabled = detect_ptp(mcu_neural_timestamps, ptp_systime)

        if ptp_enabled:
            logger.info('PTP detected')
            (non_repeat_timestamp_labels,
             non_repeat_timestamp_labels_id) = detect_trodes_time_repeats_or_frame_jumps(
                video_info.index[ptp_systime > pause_mid_time],
                frame_count[ptp_systime > pause_mid_time])
            frame_rate_from_ptp = get_framerate(
                ptp_systime[ptp_systime > pause_mid_time])
            logger.info('Camera frame rate estimated from ptp:'
                        f' {frame_rate_from_ptp:0.1f} cm/s')
            # Convert from integer nanoseconds to float seconds
            ptp_timestamps = pd.Index(
                ptp_systime[ptp_systime > pause_mid_time] /
                NANOSECONDS_PER_SECOND,
                name='time')
            position_tracking = (
                position_tracking
                .iloc[ptp_systime > pause_mid_time]
                .set_index(ptp_timestamps))

            return position_tracking
        else:
            logger.info('PTP not detected')
            camera_systime, is_valid_camera_time = estimate_camera_time_from_mcu_time(
                video_info, mcu_neural_timestamps)

            (dio_systime, frame_count,
             is_valid_camera_time, camera_systime) = remove_acquisition_timing_pause_non_ptp(
                dio_systime, frame_count, camera_systime, is_valid_camera_time,
                pause_mid_time)
            frame_rate_from_camera_systime = get_framerate(camera_systime)
            logger.info('Camera frame rate estimated from mcu timestamps:'
                        f' {frame_rate_from_camera_systime:0.1f} cm/s')

            (non_repeat_timestamp_labels,
             non_repeat_timestamp_labels_id) = detect_trodes_time_repeats_or_frame_jumps(
                video_info.index[is_valid_camera_time], frame_count)

            camera_to_mcu_lag = estimate_camera_to_mcu_lag(
                camera_systime, dio_systime, len(non_repeat_timestamp_labels_id))

            corrected_camera_systime = []
            for id in non_repeat_timestamp_labels_id:
                is_chunk = non_repeat_timestamp_labels == id
                corrected_camera_systime.append(
                    correct_timestamps_for_camera_to_mcu_lag(
                        frame_count[is_chunk], camera_systime[is_chunk],
                        camera_to_mcu_lag))
            corrected_camera_systime = np.concatenate(corrected_camera_systime)

            valid_camera_ind = np.nonzero(is_valid_camera_time)[0]
            valid_camera_ind = valid_camera_ind[non_repeat_timestamp_labels == 0]
            is_valid_camera_time[valid_camera_ind] = False

            return (position_tracking
                    .iloc[is_valid_camera_time]
                    .set_index(pd.Index(corrected_camera_systime, name='time')))


def find_camera_dio_channel(position_tracking_path, video_info):
    """Find the camera DIO by looping through all the DIOs
    and finding the right number of DIO pulses.

    Parameters
    ----------
    position_tracking_path : str
    position_tracking : pd.DataFrame, shape (n_camera_frames, 5)

    Returns
    -------
    camera_dio_times : pd.Series, shape (n_dio_pulse_state_changes,)
        Trodes time of dio ticks

    """
    head, tail = os.path.split(position_tracking_path)
    dio_paths = glob.glob(
        os.path.join(
            os.path.split(head)[0],
            tail.split('.')[0] + '.DIO',
            tail.split('.')[0] + '*.dat'))

    n_ticks = np.asarray(
        [pd.DataFrame(readTrodesExtractedDataFile(dio_file)['data']).state.sum()
         for dio_file in dio_paths])

    n_camera_frames = video_info.shape[0]
    position_ticks_file_ind = np.argmin(np.abs(n_ticks - n_camera_frames))
    camera_ticks_dio = pd.DataFrame(readTrodesExtractedDataFile(
        dio_paths[position_ticks_file_ind])['data'])

    return camera_ticks_dio.loc[camera_ticks_dio.state == 1].time


def get_video_info(position_tracking_path):
    """Get video PTP timestamps if they exist.


    Parameters
    ----------
    position_tracking_path : str

    Returns
    -------
    video_info : pd.DataFrame, shape (n_camera_frames, 2)
        PosTimestamp: unadjusted postimestamps. UINT32
        HWframeCount: integer count of frames acquired by camera
            (rolls over at 65535; can be used to detect dropped frames). UINT32
        HWTimestamp: POSIX time in nanoseconds, synchronized to PC sysclock via PTP. UINT64.

    """
    video_info = readTrodesExtractedDataFile(
        position_tracking_path.replace(
            '.pos_online.dat', '.pos_cameraHWFrameCount.dat'))
    return (pd.DataFrame(video_info['data'])
            .set_index('PosTimestamp'))


def get_mcu_neural_timestamps(position_tracking_path):
    """Neural timestamps.

    Parameters
    ----------
    position_tracking_path : str

    Returns
    -------
    mcu_neural_timestampss : pd.DataFrame
        trodestime uint32
        adjusted_systime int64

    """
    head, tail = os.path.split(position_tracking_path)
    mcu_neural_timestamps_path = os.path.join(
        os.path.split(head)[0],
        tail.split('.')[0] + '.time',
        tail.split('.')[0] + '.continuoustime.dat')
    cont_time = readTrodesExtractedDataFile(mcu_neural_timestamps_path)

    return (pd.DataFrame(cont_time['data'])
            .set_index('trodestime')
            .adjusted_systime)


def get_framerate(timestamps):
    """Frames per second"""
    timestamps = np.asarray(timestamps)
    return NANOSECONDS_PER_SECOND / np.median(np.diff(timestamps))


def find_acquisition_timing_pause(
        timestamps, min_duration=0.4, max_duration=1.0, n_search=100):
    """Landmark timing 'gap' (0.5 s pause in video stream) parameters

    Parameters
    ----------
    timestamps : int64
    min_duration : minimum duratino of gap (in seconds)
    max_duration : maximum duratino of gap (in seconds)
    n_search : search only the first `n_search` entries

    Returns
    -------
    pause_mid_time
        Midpoint time of timing pause

    """
    timestamps = np.asarray(timestamps)
    timestamp_difference = np.diff(
        timestamps[:n_search] / NANOSECONDS_PER_SECOND)
    is_valid_gap = (timestamp_difference > min_duration) & (
        timestamp_difference < max_duration)
    pause_start_ind = np.nonzero(is_valid_gap)[0][0]
    pause_end_ind = pause_start_ind + 1
    pause_mid_time = (
        timestamps[pause_start_ind] +
        (timestamps[pause_end_ind] -
         timestamps[pause_start_ind])
        // 2)

    return pause_mid_time


def find_large_frame_jumps(frame_count, min_frame_jump=15):
    """Want to avoid regressing over large frame count skips"""
    frame_count = np.asarray(frame_count)

    is_large_frame_jump = np.insert(
        np.diff(frame_count) > min_frame_jump, 0, False)

    logger.info(f'big frame jumps: {np.nonzero(is_large_frame_jump)[0]}')

    return is_large_frame_jump


def detect_trodes_time_repeats_or_frame_jumps(trodes_time, frame_count):
    """If a trodes time index repeats, then the Trodes clock has frozen
    due to headstage disconnects."""
    trodes_time = np.asarray(trodes_time)
    is_repeat_timestamp = np.insert(
        trodes_time[:-1] >= trodes_time[1:], 0, False)
    logger.info(f'repeat timestamps ind: {np.nonzero(is_repeat_timestamp)[0]}')

    is_large_frame_jump = find_large_frame_jumps(frame_count)
    is_repeat_timestamp = is_repeat_timestamp | is_large_frame_jump

    repeat_timestamp_labels = label(is_repeat_timestamp)[0]
    repeat_timestamp_labels_id, repeat_timestamp_label_counts = np.unique(
        repeat_timestamp_labels, return_counts=True)
    is_repeat = (repeat_timestamp_labels_id != 0) & (
        repeat_timestamp_label_counts > 2)
    repeat_timestamp_labels_id = repeat_timestamp_labels_id[is_repeat]
    repeat_timestamp_label_counts = repeat_timestamp_label_counts[is_repeat]
    is_repeat_timestamp[~np.isin(
        repeat_timestamp_labels, repeat_timestamp_labels_id)] = False

    non_repeat_timestamp_labels = label(~is_repeat_timestamp)[0]
    non_repeat_timestamp_labels_id = np.unique(non_repeat_timestamp_labels)
    non_repeat_timestamp_labels_id = non_repeat_timestamp_labels_id[
        non_repeat_timestamp_labels_id != 0]

    return (non_repeat_timestamp_labels,
            non_repeat_timestamp_labels_id)


def detect_ptp(mcu_neural_timestamps, ptp_time):
    """Determine if PTP was used by finding the common
    interval between the neural and camera timestamps.

    A better way to do this would be to detect it in
    the header of the .rec file"""
    mcu_neural_timestamps = np.asarray(mcu_neural_timestamps)
    ptp_time = np.asarray(ptp_time)
    common_interval_duration = (
        min(mcu_neural_timestamps[-1], ptp_time[-1]) -
        max(mcu_neural_timestamps[0], ptp_time[0]))

    return common_interval_duration > 0.0


def estimate_camera_time_from_mcu_time(video_info, mcu_neural_timestamps):
    """

    Parameters
    ----------
    video_info : pd.DataFrame
    mcu_neural_timestamps : pd.DataFrame

    Returns
    -------
    camera_systime : np.ndarray, shape (n_frames_within_neural_time,)
    is_valid_camera_time : np.ndarray, shape (n_frames,)

    """
    is_valid_camera_time = (
        (video_info.index >= mcu_neural_timestamps.index.min()) &
        (video_info.index < mcu_neural_timestamps.index.max()))
    camera_systime = np.asarray(mcu_neural_timestamps.loc[
        video_info.index[is_valid_camera_time]])

    return camera_systime, is_valid_camera_time


def estimate_camera_to_mcu_lag(camera_systime, dio_systime, n_breaks):
    if n_breaks == 0:
        dio_systime = dio_systime[:len(camera_systime)]
        camera_to_mcu_lag = np.median(camera_systime - dio_systime)
    else:
        camera_to_mcu_lag = camera_systime[0] - dio_systime[0]

    logger.info('estimated trodes to camera lag: '
                f'{camera_to_mcu_lag / NANOSECONDS_PER_SECOND:0.3f} s')
    return camera_to_mcu_lag


def remove_acquisition_timing_pause_non_ptp(
        dio_systime, frame_count, camera_systime, is_valid_camera_time,
        pause_mid_time):
    dio_systime = dio_systime[dio_systime > pause_mid_time]
    frame_count = frame_count[is_valid_camera_time][camera_systime > pause_mid_time]
    is_valid_camera_time[is_valid_camera_time] = camera_systime > pause_mid_time
    camera_systime = camera_systime[camera_systime > pause_mid_time]

    return dio_systime, frame_count, is_valid_camera_time, camera_systime


def correct_timestamps_for_camera_to_mcu_lag(
        frame_count, camera_systime, camera_to_mcu_lag):

    regression_result = linregress(
        frame_count, camera_systime - camera_to_mcu_lag)
    corrected_camera_systime = (regression_result.intercept +
                                frame_count * regression_result.slope)
    corrected_camera_systime /= NANOSECONDS_PER_SECOND

    return corrected_camera_systime


def get_cameras_ids(dataset_names, metadata):
    camera_ids = []
    for dataset_name in dataset_names:
        # extract the first the first element of the dataset_name as the epoch number
        dataset_elements = str(dataset_name).split('_')
        epoch_num = str(int(dataset_elements[0]))
        try:
            camera_ids.append(
                next(
                    task['camera_id']
                    for task in metadata['tasks']
                    if epoch_num in task['task_epochs']
                )[0]
            )
        except:
            raise InvalidMetadataException(
                'Invalid camera metadata for datasets')
    return camera_ids


def get_meters_per_pixels(cameras_ids, metadata):
    meters_per_pixels = []
    for camera_id in cameras_ids:
        try:
            meters_per_pixels.append(
                next(
                    float(camera['meters_per_pixel'])
                    for camera in metadata['cameras']
                    if camera_id == camera['id']
                )
            )
        except:
            raise InvalidMetadataException('Invalid camera metadata')
    return meters_per_pixels
