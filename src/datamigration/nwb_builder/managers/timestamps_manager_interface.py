import abc
import logging.config
import os

import numpy as np

from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TimestampManagerInterface(abc.ABC):
    def __init__(self, directories, continuous_time_directories):
        self.directories = directories
        self.continuous_time_directories = continuous_time_directories
        self.continuous_time_extractor = ContinuousTimeExtractor()
        self.timestamp_converter = TimestampConverter()

        self.number_of_datasets = self._get_number_of_datasets()
        self.file_lenghts_in_datasets = self._get_file_lenghts_in_datasets()

    @abc.abstractmethod
    def _get_timestamps(self, dataset_id):
        pass

    def read_data(self, dataset_id):
        timestamps = self._get_timestamps(dataset_id)
        continuous_time_dict = self.continuous_time_extractor.get_continuous_time_dict_file(
            self.continuous_time_directories[dataset_id])
        return self.timestamp_converter.convert_timestamps(continuous_time_dict, timestamps)

    def get_final_data_shape(self):
        return sum(self.file_lenghts_in_datasets),

    def get_directories(self):
        return self.directories

    def get_number_of_datasets(self):
        return self.number_of_datasets

    def get_file_lenghts_in_datasets(self):
        return self.file_lenghts_in_datasets

    def _get_file_lenghts_in_datasets(self):
        return [self._get_data_shape(i) for i in range(self.number_of_datasets)]

    def _get_number_of_datasets(self):
        return np.shape(self.directories)[0]

    def _get_data_shape(self, dataset_num):
        return np.shape(self.read_data(dataset_num))[0]
