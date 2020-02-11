import abc
import logging.config
import os

import numpy as np

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

    def _get_file_lenghts_in_datasets(self):
        pass

    @staticmethod
    def _convert_timestamps(continuous_time_dict, timestamps):
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

    def _get_continuous_time_dict(self, dataset_num):
        pass

    @abc.abstractmethod
    def _get_timestamps(self, dataset_num):
        pass

    @staticmethod
    def _get_number_of_datasets(directories):
        return np.shape(directories)[0]

    def _get_data_shape(self, dataset_num):
        dim1 = np.shape(self.read_data(dataset_num))[0]
        return dim1
