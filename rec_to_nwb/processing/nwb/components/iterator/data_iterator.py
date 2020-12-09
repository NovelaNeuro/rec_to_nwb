import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator


class DataIterator(AbstractDataChunkIterator):
    def __init__(self, data, number_of_channels):
        self.data = data
        self.current_number_of_rows = 0

        self._current_index = 0
        self.current_file = 0
        self.current_dataset = 0

        self.number_of_steps = self.data.get_number_of_datasets() * self.data.get_number_of_files_per_dataset()
        self.dataset_file_length = self.data.get_file_lenghts_in_datasets()
        self.number_of_files_in_single_dataset = self.data.get_number_of_files_per_dataset()
        self.shape = [self.data.get_final_data_shape()[1], number_of_channels]

    def __iter__(self):
        return self

    def _get_selection(self):
        return np.s_[sum(self.dataset_file_length[0:self.current_dataset]):
                     sum(self.dataset_file_length[0:self.current_dataset + 1]),
               (self.current_file * self.number_of_rows):
               ((self.current_file + 1) * self.number_of_rows)]

    def get_selection(self, current_dataset, dataset_file_length, number_of_new_rows):
        selection = np.s_[sum(dataset_file_length[0:current_dataset]):
                     sum(dataset_file_length[0:current_dataset + 1]),
               self.current_number_of_rows: self.current_number_of_rows + number_of_new_rows]

        self.current_number_of_rows += number_of_new_rows
        return selection

    def recommended_chunk_shape(self):
        return None

    def recommended_data_shape(self):
        return self.shape

    @property
    def dtype(self):
        return np.dtype('int16')

    @property
    def maxshape(self):
        return self.shape
