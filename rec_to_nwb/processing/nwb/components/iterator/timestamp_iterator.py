import abc

import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator


class TimestampIterator(AbstractDataChunkIterator, abc.ABC):
    def __init__(self, data):
        self.data = data
        self._current_index = 0
        self.current_dataset = 0

        self.dataset_file_lenght = data.get_file_lengths_in_datasets()
        self.number_of_steps = self.data.get_number_of_datasets()
        self.dataset_file_length = self.data.get_file_lengths_in_datasets()
        self.shape = self.data.get_final_data_shape()

    # Override
    def __iter__(self):
        return self

    @staticmethod
    def get_data_from_file(data, current_dataset):
        return data.retrieve_real_timestamps(current_dataset)

    # Override
    def recommended_chunk_shape(self):
        return None

    # Override
    def recommended_data_shape(self):
        return self.shape

    # Override
    @property
    def dtype(self):
        return np.dtype('float64')

    # Override
    @property
    def maxshape(self):
        return self.shape
