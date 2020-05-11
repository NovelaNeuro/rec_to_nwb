import numpy as np
from hdmf.data_utils import DataChunk

from rec_to_nwb.processing.nwb.components.iterator.timestamp_iterator import TimestampIterator


class SingleThreadTimestampIterator(TimestampIterator):
    # Override
    def __next__(self):
        if self._current_index < self.number_of_steps:
            data_from_file = self.__get_timestamps()
            selection = self._get_selection()
            data_chunk = DataChunk(data=data_from_file, selection=selection)

            self._current_index += 1
            self.current_dataset += 1

            del data_from_file
            return data_chunk

        raise StopIteration

    next = __next__

    def __get_timestamps(self):
        return self.data.retrieve_real_timestamps(self.current_dataset)

    def __get_selection(self):
        return np.s_[sum(self.dataset_file_lenght[0:self.current_dataset]):
                     sum(self.dataset_file_lenght[0:self.current_dataset + 1]), ]