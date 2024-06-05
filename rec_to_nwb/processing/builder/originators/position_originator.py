import glob
import logging.config
import os

import numpy as np
import pandas as pd
from pynwb import NWBFile, ProcessingModule, TimeSeries
from pynwb.behavior import Position
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile
from rec_to_nwb.processing.exceptions.invalid_metadata_exception import (
    InvalidMetadataException,
)
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from scipy.ndimage import label
from scipy.stats import linregress

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=os.path.join(str(path), os.pardir, os.pardir, os.pardir, "logging.conf"),
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)

NANOSECONDS_PER_SECOND = 1e9


class PositionOriginator:
    def __init__(
        self, datasets: list, metadata: dict, dataset_names: list, ptp_enabled: bool
    ):
        self.datasets = datasets
        self.dataset_names = dataset_names
        self.metadata = metadata
        self.pm_creator = ProcessingModule(
            "behavior", "Contains all behavior-related data"
        )
        self.ptp_enabled = ptp_enabled

    def make(self, nwb_content: NWBFile):
        position = Position(name="position")

        cameras_ids = get_cameras_ids(self.dataset_names, self.metadata)
        meters_per_pixels = get_meters_per_pixels(cameras_ids, self.metadata)

        first_timestamps = []

        for dataset_ind, dataset in enumerate(self.datasets):
            if "pos" not in dataset.data:
                logger.warning(
                    f"Dataset {dataset} does not contain position tracking data."
                )
                continue
            pos_path = dataset.data["pos"]
            conversion = meters_per_pixels[dataset_ind]
            try:
                position_tracking_path = glob.glob(
                    os.path.join(pos_path, "*.pos_online.dat")
                )
                position_df = self.get_position_with_corrected_timestamps(
                    position_tracking_path[0], self.ptp_enabled
                )
                # Multi-position split.
                # TODO: generalize key names?
                key_lists = [
                    [
                        "xloc",
                        "yloc",
                    ],  # led 0
                    [
                        "xloc2",
                        "yloc2",
                    ],
                ]  # led 1
                for led_number, valid_keys in enumerate(key_lists):
                    key_set = [
                        key for key in position_df.columns.tolist() if key in valid_keys
                    ]
                    if len(key_set) > 0:
                        position.create_spatial_series(
                            name=f"led_{led_number}_series_{dataset_ind}",
                            description=", ".join(["xloc", "yloc"]),
                            data=np.asarray(position_df[key_set]),
                            conversion=conversion,
                            reference_frame="Upper left corner of video frame",
                            timestamps=np.asarray(position_df.index),
                        )
                first_timestamps.append(position_df.index[0])
                # add the video frame index as a new processing module
                if "position_frame_index" not in nwb_content.processing:
                    nwb_content.create_processing_module(
                        name="position_frame_index",
                        description="stores video frame index for each position timestep",
                    )
                # add timeseries for each frame index set (once per series because led's share timestamps)
                nwb_content.processing["position_frame_index"].add(
                    TimeSeries(
                        name=f"series_{dataset_ind}",
                        data=np.asarray(position_df["video_frame_ind"]),
                        unit="N/A",
                        timestamps=np.asarray(position_df.index),
                    )
                )
                # add the video non-repeat timestamp labels as a new processing module
                if "non_repeat_timestamp_labels" not in nwb_content.processing:
                    nwb_content.create_processing_module(
                        name="non_repeat_timestamp_labels",
                        description="stores non_repeat_labels for each position timestep",
                    )
                # add timeseries for each non-repeat timestamp labels set (once per series because led's share timestamps)
                nwb_content.processing["non_repeat_timestamp_labels"].add(
                    TimeSeries(
                        name=f"series_{dataset_ind}",
                        data=np.asarray(position_df["non_repeat_timestamp_labels"]),
                        unit="N/A",
                        timestamps=np.asarray(position_df.index),
                    )
                )

            except IndexError:
                video_file_path = glob.glob(
                    os.path.join(pos_path, "*.pos_cameraHWFrameCount.dat")
                )
                video_df = self.get_corrected_timestamps_without_position(
                    video_file_path[0], self.ptp_enabled
                )
                position.create_spatial_series(
                    name=f"series_{dataset_ind}",
                    description=", ".join(video_df.columns.tolist()),
                    data=np.asarray(video_df),
                    conversion=conversion,
                    reference_frame="Upper left corner of video frame",
                    timestamps=np.asarray(video_df.index),
                )
                first_timestamps.append(video_df.index[0])

        # check if timestamps are in order
        first_timestamps = np.asarray(first_timestamps)
        assert np.all(first_timestamps[:-1] < first_timestamps[1:])

        logger.info("Position: Injecting into Processing Module")
        nwb_content.processing["behavior"].add(position)

    @staticmethod
    def get_position_with_corrected_timestamps(position_tracking_path, ptp_enabled):
        logger.info(os.path.split(position_tracking_path)[-1])

        # Get position tracking information
        position_tracking = pd.DataFrame(
            readTrodesExtractedDataFile(position_tracking_path)["data"]
        ).set_index("time")
        is_repeat_timestamp = detect_repeat_timestamps(position_tracking.index)
        position_tracking = position_tracking.iloc[~is_repeat_timestamp]

        # Get video information
        video_info = get_video_info(position_tracking_path)
        # On AVT cameras, HWFrame counts wraps to 0 above this value.
        AVT_camHWframeCount_wrapval = 65535
        video_info["HWframeCount"] = np.unwrap(
            video_info["HWframeCount"].astype(np.int32),
            period=AVT_camHWframeCount_wrapval,
        )

        # Keep track of video frames
        video_info["video_frame_ind"] = np.arange(len(video_info))

        # Disconnects manifest as repeats in the trodes time index
        (
            non_repeat_timestamp_labels,
            non_repeat_timestamp_labels_id,
        ) = detect_trodes_time_repeats_or_frame_jumps(
            video_info.index, video_info.HWframeCount
        )
        logging.info(f"non_repeat_timestamp_labels = {non_repeat_timestamp_labels_id}")
        video_info["non_repeat_timestamp_labels"] = non_repeat_timestamp_labels
        video_info = video_info.loc[video_info.non_repeat_timestamp_labels > 0]

        # Get the timestamps from the neural data
        mcu_neural_timestamps = get_mcu_neural_timestamps(position_tracking_path)

        # Get the camera time from the DIOs
        dio_camera_ticks = find_camera_dio_channel(position_tracking_path, video_info)
        is_valid_tick = np.isin(dio_camera_ticks, mcu_neural_timestamps.index)
        dio_systime = np.asarray(
            mcu_neural_timestamps.loc[dio_camera_ticks[is_valid_tick]]
        )

        if len(dio_systime) > 0:
            # The DIOs and camera frames are initially unaligned. There is a
            # half second pause at the start to allow for alignment.
            pause_mid_time = find_acquisition_timing_pause(dio_systime)

            # Estimate the frame rate from the DIO camera ticks as a sanity check.
            frame_rate_from_dio = get_framerate(
                dio_systime[dio_systime > pause_mid_time]
            )
            logger.info(
                "Camera frame rate estimated from DIO camera ticks:"
                f" {frame_rate_from_dio:0.1f} frames/s"
            )
        else:
            pause_mid_time = None

        # Match the camera frames to the position tracking
        # Number of video frames can be different from online tracking because
        # online tracking can be started or stopped before video is stopped.
        # Additionally, for offline tracking, frames can be skipped if the
        # frame is labeled as bad.
        video_position_info = pd.merge(
            video_info.drop(columns=[x for x in ['xloc','yloc','xloc2','yloc2'] if x in video_info.columns]),
            position_tracking, right_index=True, left_index=True, how="left"
        )   

        if ptp_enabled:
            logger.info("PTP detected")
            ptp_systime = np.asarray(video_position_info.HWTimestamp)

            if pause_mid_time is None:
                # estimate pause_mid_time from ptp timestamps if dio was missing
                pause_mid_time = find_acquisition_timing_pause(ptp_systime)

            frame_rate_from_ptp = get_framerate(
                ptp_systime[ptp_systime > pause_mid_time]
            )
            logger.info(
                "Camera frame rate estimated from PTP:"
                f" {frame_rate_from_ptp:0.1f} frames/s"
            )
            # Convert from integer nanoseconds to float seconds
            ptp_timestamps = pd.Index(ptp_systime / NANOSECONDS_PER_SECOND, name="time")
            position_tracking = video_position_info.drop(
                columns=["HWframeCount", "HWTimestamp"]
            ).set_index(ptp_timestamps)

            # Ignore positions before the timing pause.
            is_post_pause = (
                position_tracking.index > pause_mid_time / NANOSECONDS_PER_SECOND
            )
            position_tracking = position_tracking.iloc[is_post_pause]

            return position_tracking
        else:
            logger.info("PTP not detected")
            frame_count = np.asarray(video_position_info.HWframeCount)

            camera_systime, is_valid_camera_time = estimate_camera_time_from_mcu_time(
                video_position_info, mcu_neural_timestamps
            )

            (
                dio_systime,
                frame_count,
                is_valid_camera_time,
                camera_systime,
            ) = remove_acquisition_timing_pause_non_ptp(
                dio_systime,
                frame_count,
                camera_systime,
                is_valid_camera_time,
                pause_mid_time,
            )
            video_position_info = video_position_info.iloc[is_valid_camera_time]

            frame_rate_from_camera_systime = get_framerate(camera_systime)
            logger.info(
                "Camera frame rate estimated from MCU timestamps:"
                f" {frame_rate_from_camera_systime:0.1f} frames/s"
            )

            camera_to_mcu_lag = estimate_camera_to_mcu_lag(
                camera_systime, dio_systime, len(non_repeat_timestamp_labels_id)
            )

            corrected_camera_systime = []
            for id in non_repeat_timestamp_labels_id:
                is_chunk = video_position_info.non_repeat_timestamp_labels == id
                corrected_camera_systime.append(
                    correct_timestamps_for_camera_to_mcu_lag(
                        frame_count[is_chunk],
                        camera_systime[is_chunk],
                        camera_to_mcu_lag,
                    )
                )
            corrected_camera_systime = np.concatenate(corrected_camera_systime)

            return video_position_info.set_index(
                pd.Index(corrected_camera_systime, name="time")
            )

    @staticmethod
    def get_corrected_timestamps_without_position(hw_frame_count_path, ptp_enabled):
        video_info = readTrodesExtractedDataFile(hw_frame_count_path)
        video_info = pd.DataFrame(video_info["data"]).set_index("PosTimestamp")
        # On AVT cameras, HWFrame counts wraps to 0 above this value.
        AVT_camHWframeCount_wrapval = np.iinfo(np.uint16).max
        video_info["HWframeCount"] = np.unwrap(
            video_info["HWframeCount"].astype(np.int32),
            period=AVT_camHWframeCount_wrapval,
        )

        # Keep track of video frames
        video_info["video_frame_ind"] = np.arange(len(video_info))

        # Get the timestamps from the neural data
        mcu_neural_timestamps = get_mcu_neural_timestamps(hw_frame_count_path)

        # Get the camera time from the DIOs
        try:
            dio_camera_ticks = find_camera_dio_channel(hw_frame_count_path, video_info)
            is_valid_tick = np.isin(dio_camera_ticks, mcu_neural_timestamps.index)
            dio_systime = np.asarray(
                mcu_neural_timestamps.loc[dio_camera_ticks[is_valid_tick]]
            )

            # The DIOs and camera frames are initially unaligned. There is a
            # half second pause at the start to allow for alignment.
            pause_mid_time = find_acquisition_timing_pause(dio_systime)
        except IndexError:
            logger.warning("No DIO camera ticks found...")
            pause_mid_time = -1.0

            if not ptp_enabled:
                raise ValueError(
                    "No DIO camera ticks found and PTP not enabled. Cannot infer position timestamps."
                )

        if ptp_enabled:
            ptp_timestamps = pd.Index(
                video_info.HWTimestamp / NANOSECONDS_PER_SECOND, name="time"
            )
            video_info = video_info.set_index(ptp_timestamps)

            # Ignore positions before the timing pause.
            is_post_pause = video_info.index > pause_mid_time / NANOSECONDS_PER_SECOND
            video_info = video_info.iloc[is_post_pause].drop(
                columns=["HWframeCount", "HWTimestamp"]
            )
            return video_info
        else:
            raise NotImplementedError


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
            tail.split(".")[0] + ".DIO",
            tail.split(".")[0] + "*.dat",
        )
    )

    n_ticks = np.asarray(
        [
            pd.DataFrame(readTrodesExtractedDataFile(dio_file)["data"]).state.sum()
            for dio_file in dio_paths
        ]
    )

    n_camera_frames = video_info.shape[0]
    position_ticks_file_ind = np.argmin(np.abs(n_ticks - n_camera_frames))

    if (n_ticks[position_ticks_file_ind] < 0.5 * n_camera_frames) or (
        n_ticks[position_ticks_file_ind] > 1.5 * n_camera_frames
    ):
        logger.warning(
            "Likely could not find camera tick DIO channel."
            f"In the most likely dio file {dio_paths[position_ticks_file_ind]},"
            f"there are {n_ticks[position_ticks_file_ind]} ticks"
            f" and the position file has {n_camera_frames} camera frames."
        )

    camera_ticks_dio = pd.DataFrame(
        readTrodesExtractedDataFile(dio_paths[position_ticks_file_ind])["data"]
    )

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
        position_tracking_path.replace(".pos_online.dat", ".pos_cameraHWFrameCount.dat")
    )
    try:
        return pd.DataFrame(video_info["data"]).set_index("PosTimestamp")
    except:
        video_info_2 = readTrodesExtractedDataFile(
            position_tracking_path
        )
        video_info = pd.DataFrame(video_info["data"])
        video_info = video_info.rename(columns={"frameCount": "HWframeCount"})
        video_info_2 = pd.DataFrame(video_info_2["data"])
        video_info_2 = video_info_2.rename(columns={'time':"PosTimestamp"})
        
        video_info = pd.concat([video_info, video_info_2],axis=1)
        video_info = video_info.set_index("PosTimestamp")
        return video_info


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
        tail.split(".")[0] + ".time",
        tail.split(".")[0] + ".continuoustime.dat",
    )
    cont_time = readTrodesExtractedDataFile(mcu_neural_timestamps_path)

    return pd.DataFrame(cont_time["data"]).set_index("trodestime").adjusted_systime


def get_framerate(timestamps):
    """Frames per second"""
    timestamps = np.asarray(timestamps)
    return NANOSECONDS_PER_SECOND / np.median(np.diff(timestamps))


def find_acquisition_timing_pause(
    timestamps, min_duration=0.4, max_duration=1.0, n_search=100
):
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
    timestamp_difference = np.diff(timestamps[:n_search] / NANOSECONDS_PER_SECOND)
    is_valid_gap = (timestamp_difference > min_duration) & (
        timestamp_difference < max_duration
    )
    pause_start_ind = 0  # np.nonzero(is_valid_gap)[0][0]
    pause_end_ind = pause_start_ind + 1
    pause_mid_time = (
        timestamps[pause_start_ind]
        + (timestamps[pause_end_ind] - timestamps[pause_start_ind]) // 2
    )

    return pause_mid_time


def find_large_frame_jumps(frame_count, min_frame_jump=15):
    """Want to avoid regressing over large frame count skips"""
    frame_count = np.asarray(frame_count)

    is_large_frame_jump = np.insert(np.diff(frame_count) > min_frame_jump, 0, False)

    logger.info(f"big frame jumps: {np.nonzero(is_large_frame_jump)[0]}")

    return is_large_frame_jump


def detect_repeat_timestamps(timestamps):
    return np.insert(timestamps[:-1] >= timestamps[1:], 0, False)


def detect_trodes_time_repeats_or_frame_jumps(trodes_time, frame_count):
    """If a trodes time index repeats, then the Trodes clock has frozen
    due to headstage disconnects."""
    trodes_time = np.asarray(trodes_time)
    is_repeat_timestamp = detect_repeat_timestamps(trodes_time)
    logger.info(f"repeat timestamps ind: {np.nonzero(is_repeat_timestamp)[0]}")

    is_large_frame_jump = find_large_frame_jumps(frame_count)
    is_repeat_timestamp = is_repeat_timestamp | is_large_frame_jump

    repeat_timestamp_labels = label(is_repeat_timestamp)[0]
    repeat_timestamp_labels_id, repeat_timestamp_label_counts = np.unique(
        repeat_timestamp_labels, return_counts=True
    )
    is_repeat = (repeat_timestamp_labels_id != 0) & (repeat_timestamp_label_counts > 2)
    repeat_timestamp_labels_id = repeat_timestamp_labels_id[is_repeat]
    repeat_timestamp_label_counts = repeat_timestamp_label_counts[is_repeat]
    is_repeat_timestamp[
        ~np.isin(repeat_timestamp_labels, repeat_timestamp_labels_id)
    ] = False

    non_repeat_timestamp_labels = label(~is_repeat_timestamp)[0]
    non_repeat_timestamp_labels_id = np.unique(non_repeat_timestamp_labels)
    non_repeat_timestamp_labels_id = non_repeat_timestamp_labels_id[
        non_repeat_timestamp_labels_id != 0
    ]

    return (non_repeat_timestamp_labels, non_repeat_timestamp_labels_id)


def detect_ptp(mcu_neural_timestamps, ptp_time):
    """Determine if PTP was used by finding the common
    interval between the neural and camera timestamps.

    A better way to do this would be to detect it in
    the header of the .rec file"""
    mcu_neural_timestamps = np.asarray(mcu_neural_timestamps)
    ptp_time = np.asarray(ptp_time)
    common_interval_duration = min(
        np.max(mcu_neural_timestamps), np.max(ptp_time)
    ) - max(np.min(mcu_neural_timestamps), np.min(ptp_time))

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
    is_valid_camera_time = np.isin(video_info.index, mcu_neural_timestamps.index)
    camera_systime = np.asarray(
        mcu_neural_timestamps.loc[video_info.index[is_valid_camera_time]]
    )

    return camera_systime, is_valid_camera_time


def estimate_camera_to_mcu_lag(camera_systime, dio_systime, n_breaks):
    if n_breaks == 0:
        dio_systime = dio_systime[: len(camera_systime)]
        camera_to_mcu_lag = np.median(camera_systime - dio_systime)
    else:
        camera_to_mcu_lag = camera_systime[0] - dio_systime[0]

    logger.info(
        "estimated trodes to camera lag: "
        f"{camera_to_mcu_lag / NANOSECONDS_PER_SECOND:0.3f} s"
    )
    return camera_to_mcu_lag


def remove_acquisition_timing_pause_non_ptp(
    dio_systime, frame_count, camera_systime, is_valid_camera_time, pause_mid_time
):
    dio_systime = dio_systime[dio_systime > pause_mid_time]
    frame_count = frame_count[is_valid_camera_time][camera_systime > pause_mid_time]
    is_valid_camera_time[is_valid_camera_time] = camera_systime > pause_mid_time
    camera_systime = camera_systime[camera_systime > pause_mid_time]

    return dio_systime, frame_count, is_valid_camera_time, camera_systime


def correct_timestamps_for_camera_to_mcu_lag(
    frame_count, camera_systime, camera_to_mcu_lag
):
    regression_result = linregress(frame_count, camera_systime - camera_to_mcu_lag)
    corrected_camera_systime = (
        regression_result.intercept + frame_count * regression_result.slope
    )
    corrected_camera_systime /= NANOSECONDS_PER_SECOND

    return corrected_camera_systime


def get_cameras_ids(dataset_names, metadata):
    camera_ids = []
    for dataset_name in dataset_names:
        # extract the first the first element of the dataset_name as the epoch number
        dataset_elements = str(dataset_name).split("_")
        epoch_num = str(int(dataset_elements[0]))
        try:
            camera_ids.append(
                next(
                    task["camera_id"]
                    for task in metadata["tasks"]
                    if epoch_num in task["task_epochs"]
                )[0]
            )
        except Exception as e:
            print(e)
            raise InvalidMetadataException("Invalid camera metadata for datasets")
    return camera_ids


def get_meters_per_pixels(cameras_ids, metadata):
    meters_per_pixels = []
    for camera_id in cameras_ids:
        try:
            meters_per_pixels.append(
                next(
                    float(camera["meters_per_pixel"])
                    for camera in metadata["cameras"]
                    if camera_id == camera["id"]
                )
            )
        except Exception as e:
            print(e)
            raise InvalidMetadataException("Invalid camera metadata")
    return meters_per_pixels
