import concurrent.futures

import numpy as np
from hdmf.data_utils import DataChunk

from rec_to_nwb.processing.nwb.components.iterator.data_iterator_pos import DataIteratorPos


class MultiThreadDataIteratorPos(DataIteratorPos):
    def __init__(self, data, number_of_threads=6):
        DataIteratorPos.__init__(self, data)
        self.number_of_threads = number_of_threads

    def __next__(self):
        if self._current_index < self.number_of_steps:
            number_of_threads_in_current_step = min(self.number_of_threads,
                                                    self.number_of_files_in_single_dataset - self.current_file)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                threads = [executor.submit(MultiThreadDataIteratorPos.get_data_from_file,
                                           self.data, self.current_dataset, self.current_file + i)
                           for i in range(number_of_threads_in_current_step)]
            data_from_multiple_files = ()
            for thread in threads:
                data_from_multiple_files += (thread.result(),)
            stacked_data_from_multiple_files = np.hstack(data_from_multiple_files)
            selection = self.get_selection(number_of_threads=number_of_threads_in_current_step,
                                           current_dataset=self.current_dataset,
                                           dataset_file_length=self.dataset_file_length,
                                           current_file=self.current_file,
                                           number_of_rows=self.number_of_rows)
            data_chunk = DataChunk(data=stacked_data_from_multiple_files, selection=selection)

            self._current_index += number_of_threads_in_current_step
            self.current_file += number_of_threads_in_current_step

            if self.current_file >= self.number_of_files_in_single_dataset:
                self.current_dataset += 1
                self.current_file = 0
                self.current_number_of_rows = 0

            del stacked_data_from_multiple_files
            return data_chunk

        raise StopIteration

    next = __next__

    @staticmethod
    def get_data_from_file(data, current_dataset, current_file):
        return np.transpose(data.read_data(current_dataset, current_file))

