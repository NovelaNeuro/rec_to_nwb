import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator


class DataIterator(AbstractDataChunkIterator):
    def __init__(self, data):
        self.data = data

        self._current_index = 0
        self.current_file = 0
        self.current_dataset = 0

        self.number_of_datasets = self.data.get_number_of_datasets() 
        self.number_of_steps = self.number_of_datasets * self.data.get_number_of_files_per_dataset()
        self.dataset_file_length = self.data.get_file_lenghts_in_datasets()
        self.number_of_rows = self.data.get_number_of_rows_per_file()
        self.number_of_files_in_single_dataset = self.data.get_number_of_files_per_dataset()
        self.shape = [self.data.get_final_data_shape()[1], self.data.get_final_data_shape()[0]]

    def __iter__(self):
        return self

    def _get_selection(self):
        if isinstance(self.number_of_rows, int):
            # single number (legacy behavior)
            start_index = (self.current_file * self.number_of_rows)
            stop_index = ((self.current_file + 1) * self.number_of_rows)
        else:
            # expecting a list (different number_of_rows for each file)
            start_index = sum(self.number_of_rows[0:self.current_file])
            stop_index = sum(self.number_of_rows[0:(self.current_file + 1)])
        return np.s_[sum(self.dataset_file_length[0:self.current_dataset]):
                     sum(self.dataset_file_length[0:self.current_dataset + 1]),
               start_index:
               stop_index]

    @staticmethod
    def get_selection(number_of_threads, current_dataset, dataset_file_length, current_file, number_of_rows):
        if isinstance(number_of_rows, int):
            # single number (legacy behavior)
            start_index = (current_file * number_of_rows)
            stop_index = ((current_file + number_of_threads) * number_of_rows)
        else:
            # expecting a list (different number_of_rows for each file)
            start_index = sum(number_of_rows[0:current_file])
            stop_index = sum(number_of_rows[0:(current_file + number_of_threads)])
        return np.s_[sum(dataset_file_length[0:current_dataset]):
                     sum(dataset_file_length[0:current_dataset + 1]),
               start_index:
               stop_index]

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
