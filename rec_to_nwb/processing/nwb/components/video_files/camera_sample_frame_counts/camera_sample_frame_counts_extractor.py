import glob
import os

import numpy as np
import pandas as pd
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
        return glob.glob(
            os.path.join(self.raw_data_path, '*.videoTimeStamps.cameraHWSync'))

    def __get_all_hwframecount_files(self):
        return glob.glob(
            os.path.join(self.raw_data_path,
                         '*.videoTimeStamps.cameraHWFrameCount'))

    @staticmethod
    def __merge_data_from_multiple_files(data):
        return np.vstack(data)

    def __extract_single(self, hw_frame_count_filename):
        content = pd.DataFrame(
            readTrodesExtractedDataFile(
                os.path.join(self.raw_data_path, hw_frame_count_filename)
            )["data"])
        try:
            # columns: frame count, timestamps
            return content.iloc[:, [1, 0]].to_numpy()
        except IndexError:
            return np.vstack((content.iloc[:, 0].to_numpy(),  # frame counts
                              np.arange(len(content)))  # dummy timestamps
                             ).T.astype(np.uint32)
