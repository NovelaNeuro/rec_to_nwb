import numpy as np
from hdmf.data_utils import DataChunk

from lf.datamigration.nwb.components.iterator.data_iterator import DataIterator


class SingleThreadDataIterator(DataIterator):

    def __init__(self, data):
        DataIterator.__init__(self, data)

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < self.number_of_steps:
            data_from_file = self.__get_data_from_file()
            selection = self._get_selection()
            data_chunk = DataChunk(data=data_from_file, selection=selection)

            self._current_index += 1
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
