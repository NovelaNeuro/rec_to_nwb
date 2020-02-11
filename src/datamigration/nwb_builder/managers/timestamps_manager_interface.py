import abc
import logging.config
import os

import numpy as np
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TimestampManagerInterface(abc.ABC):
    @abc.abstractmethod
    def read_data(self, dataset_num):
        pass

    @abc.abstractmethod
    def get_final_data_shape(self):
        pass

    @abc.abstractmethod
    def __get_file_lenghts_in_datasets(self):
        return [self.__get_data_shape(i) for i in range(self.number_of_datasets)]

    @staticmethod
    @abc.abstractmethod
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

    @abc.abstractmethod
    def __get_continuous_time_dict(self, dataset_num):
        continuous_time = readTrodesExtractedDataFile(self.continuous_time_directories[dataset_num])
        continuous_time_dict = {str(data[0]): float(data[1]) for data in continuous_time['data']}
        return continuous_time_dict

    @abc.abstractmethod
    def __get_timestamps(self, dataset_num):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_num][0])
        position = pd.DataFrame(pos_online['data'])
        timestamps = position.time.to_numpy(dtype='int64')
        return timestamps

    @staticmethod
    @abc.abstractmethod
    def __get_num_datasets(directories):
        return np.shape(directories)[0]

    @abc.abstractmethod
    def __get_data_shape(self, dataset_num):
        dim1 = np.shape(self.read_data(dataset_num))[0]
        return dim1
