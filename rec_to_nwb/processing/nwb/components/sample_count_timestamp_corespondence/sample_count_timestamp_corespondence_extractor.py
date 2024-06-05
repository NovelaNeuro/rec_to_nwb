import numpy as np
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class SampleCountTimestampCorespondenceExtractor:
    def __init__(self, files):
        self.files = files

    def extract(self):
        data = []
        for file in self.files:
            data.append(self.__get_continuous_time_data_from_single_file(file))
        merged_data = self.__merge_data_from_multiple_files(data)
        return merged_data

    def __merge_data_from_multiple_files(self, data):
        merged_data = np.vstack(data)
        return merged_data

    def __get_continuous_time_data_from_single_file(self, continuous_time_file):
        continuous_time = readTrodesExtractedDataFile(continuous_time_file)
        new_array = np.ndarray(
            shape=(len(continuous_time['data']), 2), dtype='int64')
        new_array[:, 0] = continuous_time['data']['trodestime']
        new_array[:, 1] = continuous_time['data']['adjusted_systime']

        # for i, single_timestamp in enumerate(continuous_time['data']):
        #     new_array[i, 0] = single_timestamp[0]
        #     new_array[i, 1] = single_timestamp[3]
        return new_array
