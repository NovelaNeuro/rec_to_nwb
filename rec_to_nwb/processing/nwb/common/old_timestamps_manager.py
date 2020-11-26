import abc
import logging.config
import os

import numpy as np


path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class OldTimestampManager(abc.ABC):
    def __init__(self, directories):
        self.directories = directories
        self.number_of_datasets = self._get_number_of_datasets()
        self.file_lenghts_in_datasets = self.__calculate_file_lenghts_in_datasets()

    @abc.abstractmethod
    def _get_timestamps(self, dataset_id):
        pass

    def retrieve_real_timestamps(self, dataset_id):
        timestamps_ids = self.read_timestamps_ids(dataset_id)
        converted_timestamps = np.ndarray(shape=[len(timestamps_ids), ], dtype="float64")
        for i, _ in enumerate(timestamps_ids):
            value = float('nan')  # just a dummy value for now
            converted_timestamps[i] = value
        return converted_timestamps

    def read_timestamps_ids(self, dataset_id):
        return self._get_timestamps(dataset_id)

    def get_final_data_shape(self):
        return sum(self.file_lenghts_in_datasets),

    def get_number_of_datasets(self):
        return self.number_of_datasets

    def get_file_lenghts_in_datasets(self):
        return self.file_lenghts_in_datasets

    def __calculate_file_lenghts_in_datasets(self):
        return [self._get_data_shape(i) for i in range(self.number_of_datasets)]

    def _get_number_of_datasets(self):
        return np.shape(self.directories)[0]

    def _get_data_shape(self, dataset_num):
        return np.shape(self.read_timestamps_ids(dataset_num))[0]
