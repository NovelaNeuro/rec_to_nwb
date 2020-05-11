import concurrent.futures

import numpy as np
from hdmf.data_utils import DataChunk

from rec_to_nwb.processing.nwb.components.iterator.timestamp_iterator import TimestampIterator


class MultiThreadTimestampIterator(TimestampIterator):

    def __init__(self, data, number_of_threads=6):
        TimestampIterator.__init__(self, data)
        self.number_of_threads = number_of_threads

    # Override
    def __next__(self):
        if self._current_index < self.number_of_steps:
            number_of_threads_in_current_step = min(self.number_of_threads,
                                                    self.number_of_steps - self._current_index)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                threads = [executor.submit(MultiThreadTimestampIterator.get_data_from_file,
                                           self.data, self.current_dataset + i)
                           for i in range(number_of_threads_in_current_step)]
            data_from_multiple_files = ()
            for thread in threads:
                data_from_multiple_files += (thread.result(),)
            stacked_data_from_multiple_files = np.hstack(data_from_multiple_files)
            selection = self.__get_selection(number_of_threads_in_current_step)
            data_chunk = DataChunk(data=stacked_data_from_multiple_files, selection=selection)

            self._current_index += number_of_threads_in_current_step
            self.current_dataset += number_of_threads_in_current_step

            del stacked_data_from_multiple_files
            return data_chunk

        raise StopIteration

    next = __next__

    def __get_selection(self, number_of_threads_in_current_step):
        return np.s_[sum(self.dataset_file_lenght[0:self.current_dataset]):
                     sum(self.dataset_file_lenght[0:self.current_dataset + number_of_threads_in_current_step]), ]