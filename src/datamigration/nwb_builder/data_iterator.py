import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator, DataChunk


class DataIterator(AbstractDataChunkIterator):

    def __init__(self, data):
        self.data = data
        self.files = data.directories
        self.num_steps = data.num_datasets * data.single_dataset_len
        self.__curr_index = 0
        self.current_file = 0
        self.current_dataset = 0
        self.dataset_file_lenght = data.file_lenghts
        self.num_rows = data.num_rows_per_file
        self.num_files_in_single_dataset = data.single_dataset_len
        self.shape = data.get_final_data_shape()

    def __iter__(self):
        return self

    def __next__(self):
        if self.__curr_index < self.num_steps:
            new_data = self.data.read_data(self.current_dataset, self.current_file)
            chunk = DataChunk(data=new_data,
                              selection=np.s_[(self.current_file * self.num_rows):
                                              ((self.current_file + 1) * self.num_rows),
                                        sum(self.dataset_file_lenght[0:self.current_dataset]):
                                        sum(self.dataset_file_lenght[0:self.current_dataset + 1])])
            self.__curr_index += 1
            self.current_file += 1
            if self.current_file >= self.num_files_in_single_dataset:
                self.current_dataset += 1
                self.current_file = 0
            del new_data
            return chunk
        raise StopIteration

    next = __next__

    def recommended_chunk_shape(self):
        return None  # Use autochunking

    def recommended_data_shape(self):
        return self.shape

    @property
    def dtype(self):
        return np.dtype('int16')

    @property
    def maxshape(self):
        return self.shape


class DataIterator1D(AbstractDataChunkIterator):

    def __init__(self, data):
        self.data = data
        self.files = data.directories
        self.num_steps = data.num_datasets * data.single_dataset_len
        self.__curr_index = 0
        self.current_file = 0
        self.current_dataset = 0
        self.dataset_file_lenght = data.file_lenghts
        self.num_rows = data.num_rows_per_file
        self.num_files_in_single_dataset = data.single_dataset_len
        self.shape = None,

    def __iter__(self):
        return self

    def __next__(self):
        if self.__curr_index < self.num_steps:
            new_data = self.data.read_data(self.current_dataset, self.current_file)
            chunk = DataChunk(data=new_data,
                              selection=np.s_[None,
                                        sum(self.dataset_file_lenght[0:self.current_dataset]):
                                        sum(self.dataset_file_lenght[0:self.current_dataset + 1])])
            self.__curr_index += 1
            self.current_file += 1
            if self.current_file >= self.num_files_in_single_dataset:
                self.current_dataset += 1
                self.current_file = 0
            del new_data
            return chunk
        raise StopIteration

    next = __next__

    def recommended_chunk_shape(self):
        return None  # Use autochunking

    def recommended_data_shape(self):
        return self.shape

    @property
    def dtype(self):
        return np.dtype('int16')

    @property
    def maxshape(self):
        return self.shape
