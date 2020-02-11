import logging.config
import os

import numpy as np
import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.managers.timestamps_manager_interface import TimestampManagerInterface

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PosTimestampManager(TimestampManagerInterface):
    def __init__(self, directories, continuous_time_directories):
        self.directories = directories
        self.continuous_time_directories = continuous_time_directories

        self.number_of_datasets = self.__get_num_datasets(self.directories)
        self.file_lenghts_in_datasets = self.__get_file_lenghts_in_datasets()

    def __get_file_lenghts_in_datasets(self):
        return [self.__get_data_shape(i) for i in range(self.number_of_datasets)]

    @staticmethod
    def __convert_timestamps(continuous_time_dict, timestamps):
        converted_timestamps = np.ndarray([np.shape(timestamps)[0], ], dtype="float64")
        for i in range(np.shape(timestamps)[0]):
            key = str(timestamps[i])
            try:
                value = continuous_time_dict[key]
                converted_timestamps[i] = float(value) / 1E9
            except KeyError as error:
                message = 'Following key: ' + str(key) + ' does not exist!' + str(error)
                logger.exception(message)
                converted_timestamps[i] = float('nan')
        return converted_timestamps

    def __get_continuous_time_dict(self, dataset_num):
        continuous_time = readTrodesExtractedDataFile(self.continuous_time_directories[dataset_num])
        continuous_time_dict = {str(data[0]): float(data[1]) for data in continuous_time['data']}
        return continuous_time_dict

    def __get_timestamps(self, dataset_num):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_num][0])
        position = pd.DataFrame(pos_online['data'])
        timestamps = position.time.to_numpy(dtype='int64')
        return timestamps

    @staticmethod
    def __get_num_datasets(directories):
        return np.shape(directories)[0]

    def __get_data_shape(self, dataset_num):
        dim1 = np.shape(self.read_data(dataset_num))[0]
        return dim1

    # override
    def read_data(self, dataset_num):
        timestamps = self.__get_timestamps(dataset_num)
        continuous_time_dict = self.__get_continuous_time_dict(dataset_num)
        converted_timestamps = self.__convert_timestamps(continuous_time_dict, timestamps)
        return converted_timestamps

    # override
    def get_final_data_shape(self):
        return sum(self.file_lenghts_in_datasets),
