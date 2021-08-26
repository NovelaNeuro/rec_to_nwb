"""Returns the video frame counts and timestamps for all epochs."""
import glob
import os

import numpy as np
import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class CameraSampleFrameCountsExtractor:
    def __init__(self, raw_data_path):
        self.raw_data_path = raw_data_path

    def extract(self):
        """Returns the video frame counts and timestamps for all epochs.

        If precision time protocol (PTP) timestamps do not exist, then
        timestamps are simply just a count of the frames in that epoch.
        """
        files = glob.glob(
            os.path.join(self.raw_data_path, '*.videoTimeStamps.cameraHWSync'))
        if len(files) == 0:
            # in case of old dataset
            files = glob.glob(
                os.path.join(self.raw_data_path,
                             '*.videoTimeStamps.cameraHWFrameCount'))
        return np.vstack([self.__extract_single(file) for file in files])

    def __extract_single(self, filename):
        """Returns the video frame counts and timestamps for a single epoch."""
        content = pd.DataFrame(
            readTrodesExtractedDataFile(
                os.path.join(self.raw_data_path, filename)
            )["data"])
        try:
            # columns: frame count, timestamps
            return content.iloc[:, [1, 0]].to_numpy()
        except IndexError:
            return np.vstack((content.iloc[:, 0].to_numpy(),  # frame counts
                              np.arange(len(content)))  # dummy timestamps
                             ).T.astype(np.uint32)
