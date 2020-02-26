import concurrent.futures

import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator, DataChunk


class MultiThreadDataIterator(AbstractDataChunkIterator):

    def __init__(self, data, number_of_threads=6):
        self.data = data
        self.number_of_threads = number_of_threads

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
            number_of_threads_in_current_step = min(self.number_of_threads,
                                                    self.number_of_files_in_single_dataset - self.current_file)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    threads = [executor.submit(MultiThreadDataIterator.get_data_from_file,
                                               data=self.data,
                                               current_dataset=self.current_dataset + i)
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

            self.__current_index += number_of_threads_in_current_step
            self.current_file += number_of_threads_in_current_step

            if self.current_file >= self.number_of_files_in_single_dataset:
                self.current_dataset += 1
                self.current_file = 0

            del stacked_data_from_multiple_files
            return data_chunk

        raise StopIteration

    next = __next__

    @staticmethod
    def get_data_from_file(data, current_dataset, current_file):
        return np.transpose(data.read_data(current_dataset, current_file))

    @staticmethod
    def get_selection(number_of_threads, current_dataset, dataset_file_length, current_file, number_of_rows):
        return np.s_[sum(dataset_file_length[0:current_dataset]):
                     sum(dataset_file_length[0:current_dataset + 1]),
               (current_file * number_of_rows):
               ((current_file + number_of_threads) * number_of_rows)]

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
