import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor
from fl.datamigration.processing.timestamp_converter import TimestampConverter


class FlInvalidTimePosTimestampExtractor:
    def __init__(self, datasets):
        self.datasets = datasets

    def get_converted_timestamps(self):
        return self.__convert_timestamps(self.__read_pos_timestamps(), self.__get_continuous_time_dicts())

    def __convert_timestamps(self, timestamps, continuous_time_dicts):
        return [TimestampConverter.convert_timestamps(continuous_time_dicts[i], timestamp)
                for i, timestamp in enumerate(timestamps)]

    def __read_pos_timestamps(self):
        timestamp_files = self.__get_pos_files()
        return [self.__read_single_pos_timestamps(timestamp_file) for timestamp_file in timestamp_files]

    def __get_pos_files(self):
        all_files = []
        for dataset in self.datasets:
            single_dataset_files = dataset.get_all_data_from_dataset('pos')
            for file in single_dataset_files:
                if file.endswith('pos_online.dat'):
                    all_files.append(dataset.get_data_path_from_dataset('pos') + file)
        return all_files

    def __read_single_pos_timestamps(self, timestamp_file):
        pos_online = readTrodesExtractedDataFile(timestamp_file)
        position = pd.DataFrame(pos_online['data'])
        return position.time.to_numpy(dtype='int64')


    def __get_continuous_time_dicts(self):
        continuous_time_extractor = ContinuousTimeExtractor()
        continuous_time_files = [dataset.get_continuous_time() for dataset in self.datasets]
        return continuous_time_extractor.get_continuous_time_dict(continuous_time_files)
