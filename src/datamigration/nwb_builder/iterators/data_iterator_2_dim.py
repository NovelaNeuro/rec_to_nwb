import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator, DataChunk


class DataIterator2D(AbstractDataChunkIterator):

    def __init__(self, data):
        self.data = data

        self.__current_index = 0
        self.current_file = 0
        self.current_dataset = 0

        self.files = self.__get_files(data)
        self.number_of_steps = self.__get_all_files_from_all_datasets(data)
        self.dataset_file_length = self.__get_dataset_file_length(data)
        self.number_of_rows = self.__get_number_of_rows(data)
        self.number_of_files_in_single_dataset = self.__get_number_of_files_in_single_dataset(data)
        self.data_shape = self.__get_data_shape(data)

    @staticmethod
    def __get_files(data):
        return data.directories

    @staticmethod
    def __get_all_files_from_all_datasets(data):
        return data.number_of_datasets * data.number_of_files_per_dataset

    @staticmethod
    def __get_dataset_file_length(data):
        return data.file_lenghts_in_datasets

    @staticmethod
    def __get_number_of_rows(data):
        return data.number_of_rows_per_file

    @staticmethod
    def __get_number_of_files_in_single_dataset(data):
        return data.number_of_files_per_dataset

    @staticmethod
    def __get_data_shape(data):
        return [data.get_final_data_shape()[1], data.get_final_data_shape()[0]]

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
        return self.data_shape

    # Override
    @property
    def dtype(self):
        return np.dtype('int16')

    # Override
    @property
    def maxshape(self):
        return self.data_shape


