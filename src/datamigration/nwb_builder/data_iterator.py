import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator, DataChunk


class DataIterator(AbstractDataChunkIterator):

    def __init__(self, channel_files, num_steps):
        self.shape = (4, num_steps * len(channel_files))
        self.channel_files = channel_files
        self.num_steps = num_steps
        self.__curr_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__curr_index < len(self.channel_files):
            newfp = np.memmap(self.channel_files[self.__curr_index],
                              dtype='int16', mode='r', shape=(4, self.num_steps))
            data = DataChunk(data=newfp,
                             selection=np.s_[:, ((self.__curr_index) *
                                                 self.num_steps):((((self.__curr_index) + 1) * self.num_steps))])
            self.__curr_index += 1
            del newfp
            return data
        else:
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
