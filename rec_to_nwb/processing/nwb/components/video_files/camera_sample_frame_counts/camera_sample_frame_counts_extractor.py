import os

import numpy as np
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class CameraSampleFrameCountsExtractor:
    def __init__(self, raw_data_path):
        self.raw_data_path = raw_data_path

    def extract(self):
        data = []
        files = self.__get_all_hwsync_files()
        if len(files) == 0:
            # in case of old dataset
            files = self.__get_all_hwframecount_files()
        for file in files:
            data.append(self.__extract_single(file))
        merged_data = self.__merge_data_from_multiple_files(data)
        return merged_data

    def __get_all_hwsync_files(self):
        all_files = os.listdir(self.raw_data_path)
        hwsync_files = []
        for file in all_files:
            if 'videoTimeStamps.cameraHWSync' in file:
                hwsync_files.append(file)
        return hwsync_files

    def __get_all_hwframecount_files(self):
        all_files = os.listdir(self.raw_data_path)
        hwframecount_files = []
        for file in all_files:
            if 'videoTimeStamps.cameraHWFrameCount' in file:
                hwframecount_files.append(file)
        return hwframecount_files

    @staticmethod
    def __merge_data_from_multiple_files(data):
        merged_data = np.vstack(data)
        return merged_data

    def __extract_single(self, hw_frame_count_filename):
        content = readTrodesExtractedDataFile(
            self.raw_data_path + "/" + hw_frame_count_filename
        )["data"]
        camera_sample_frame_counts = np.ndarray(
            shape=(len(content), 2), dtype='uint32')
        for i, record in enumerate(content):
            if len(record) > 1:
                # from cameraHWSync
                camera_sample_frame_counts[i, 0] = record[1]  # framecounts
                camera_sample_frame_counts[i, 1] = record[0]  # timestamps
            else:
                # from cameraHWFrameCount (old dataset)
                camera_sample_frame_counts[i, 0] = record[0]  # framecounts
                # timestamps (dummy)
                camera_sample_frame_counts[i, 1] = i
        return camera_sample_frame_counts
