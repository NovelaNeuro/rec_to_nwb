import logging.config
import os
import numpy as np
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from rec_to_nwb.processing.tools.beartype.beartype import beartype

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class FlVideoFilesExtractor:

    @beartype
    def __init__(self, raw_data_path: str, video_files_metadata: list,
                    convert_timestamps: bool = True,
                    return_timestamps: bool = True):
        self.raw_data_path = raw_data_path
        self.video_files_metadata = video_files_metadata
        self.convert_timestamps = convert_timestamps
        self.return_timestamps = return_timestamps

    def extract_video_files(self):
        video_files = self.video_files_metadata
        extracted_video_files = []
        for video_file in video_files:
            if self.return_timestamps:
                timestamps = self._get_timestamps(video_file)
            else:
                timestamps = np.array([])
            new_fl_video_file = {
                "name": video_file["name"],
                "timestamps": timestamps,
                "device": video_file["camera_id"]
            }
            extracted_video_files.append(new_fl_video_file)
        return extracted_video_files

    def _get_timestamps(self, video_file):
        try:
            video_timestamps = self._read_video_timestamps_hw_sync(video_file)
            logger.info('Loaded cameraHWSync timestamps for {}'.format(video_file['name'][:-4]))
            is_old_dataset = False
        except FileNotFoundError:
            # old dataset
            video_timestamps = self._read_video_timestamps_hw_framecount(video_file)
            logger.info('Loaded cameraHWFrameCount for {} (old dataset)'.format(video_file['name'][:-4]))
            is_old_dataset = True
        # the timestamps array from the cam
        if is_old_dataset or (not self.convert_timestamps):
            # for now, FORCE turn off convert_timestamps for old dataset
            return video_timestamps
        return self._convert_timestamps(video_timestamps)

    def _read_video_timestamps_hw_sync(self, video_file):
        return readTrodesExtractedDataFile(
                self.raw_data_path + "/"
                + video_file["name"][:-4]
                + "videoTimeStamps.cameraHWSync")['data']['HWTimestamp']

    def _read_video_timestamps_hw_framecount(self, video_file):
        return readTrodesExtractedDataFile(
                self.raw_data_path + "/"
                + video_file["name"][:-4]
                + "videoTimeStamps.cameraHWFrameCount")['data']['frameCount']

    def _convert_timestamps(self, timestamps):
        #converted_timestamps = np.ndarray(shape=np.shape(timestamps), dtype='float64')
        converted_timestamps = timestamps / 1E9
        # for i, record in enumerate(timestamps):
        #     converted_timestamps[i] = record[2]/1E9
        return converted_timestamps
