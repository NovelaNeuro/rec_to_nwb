import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator, DataChunk


class SingleThreadDataIterator(AbstractDataChunkIterator):

    def __init__(self, data):
        self.data = data

        self.__current_index = 0
        self.current_file = 0
        self.current_dataset = 0

        self.number_of_steps = self.data.get_number_of_datasets() * self.data.get_number_of_files_per_dataset()
        self.dataset_file_length = self.data.get_file_lenghts_in_datasets()
        self.number_of_rows = self.data.get_number_of_rows_per_file()
        self.number_of_files_in_single_dataset = self.data.get_number_of_files_per_dataset()
        self.shape = [self.data.get_final_data_shape()[1], self.data.get_final_data_shape()[0]]

    # Override
    def __iter__(self):
        return self

    # Override
    def __next__(self):
        if self.__current_index < self.number_of_steps:
            data_from_file = self.__get_data_from_file()
            selection = self.__get_selection()
            data_chunk = DataChunk(data=data_from_file, selection=selection)

            self.__current_index += 1
            self.current_file += 1

            if self.current_file >= self.number_of_files_in_single_dataset:
                self.current_dataset += 1
                self.current_file = 0

            del data_from_file
            return data_chunk

        raise StopIteration

    next = __next__

    def __get_data_from_file(self):
        return np.transpose(self.data.read_data(self.current_dataset, self.current_file))

    def __get_selection(self):
        return np.s_[sum(self.dataset_file_length[0:self.current_dataset]):
                     sum(self.dataset_file_length[0:self.current_dataset + 1]),
               (self.current_file * self.number_of_rows):
               ((self.current_file + 1) * self.number_of_rows)]

    # Override
    def recommended_chunk_shape(self):
        return None

    # Override
    def recommended_data_shape(self):
        return self.shape

    # Override
    @property
    def dtype(self):
        return np.dtype('int16')

    # Override
    @property
    def maxshape(self):
        return self.shape
