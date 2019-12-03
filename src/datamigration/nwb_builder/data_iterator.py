import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator, DataChunk
from mountainlab_pytools.mdaio import readmda

class DataIterator(AbstractDataChunkIterator):

    def __init__(self, path_to_files, channel_files, num_steps, num_rows, num_datasets):
        self.shape = (num_rows * len(channel_files), num_steps * num_datasets)
        self.channel_files = channel_files
        self.num_steps = num_steps
        self.num_datasets = num_datasets
        self.__curr_index = 0
        self.__curr_dataset = 0
        self.num_rows = num_rows

    def __iter__(self):
        return self

    def __next__(self):
        if self.__curr_index < len(self.channel_files):
            new_data = readmda(self.channel_files[self.__curr_index])
            chunk = DataChunk(data=new_data,
                              selection=np.s_[((self.__curr_index) * self.num_rows):
                                              ((((self.__curr_index) + 1) * self.num_rows)),
                                        (self.__curr_dataset * self.num_steps):
                                        ((self.__curr_dataset + 1) *
                                         self.num_steps)])
            self.__curr_index += 1
            if self.__curr_index >= self.len(self.channel_files):
                self.__curr_dataset += 1
                self.__curr_index = 0
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
