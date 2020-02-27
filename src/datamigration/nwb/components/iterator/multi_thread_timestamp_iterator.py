import concurrent.futures

import numpy as np
from hdmf.data_utils import AbstractDataChunkIterator, DataChunk


class MultiThreadTimestampIterator(AbstractDataChunkIterator):

    def __init__(self, data, number_of_threads=6):
        self.data = data
        self.number_of_threads = number_of_threads
        self.__current_index = 0
        self.current_dataset = 0

        self.dataset_file_lenght = data.get_file_lenghts_in_datasets()
        self.number_of_steps = self.data.get_number_of_datasets()
        self.dataset_file_length = self.data.get_file_lenghts_in_datasets()
        self.shape = self.data.get_final_data_shape()

    # Override
    def __iter__(self):
        return self

    # Override
    def __next__(self):
        if self.__current_index < self.number_of_steps:
            number_of_threads_in_current_step = min(self.number_of_threads,
                                                    self.number_of_steps - self.__current_index)

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

            self.__current_index += number_of_threads_in_current_step
            self.current_dataset += number_of_threads_in_current_step

            del stacked_data_from_multiple_files
            return data_chunk

        raise StopIteration

    next = __next__

    @staticmethod
    def get_data_from_file(data, current_dataset):
        return data.retrieve_real_timestamps(current_dataset)

    def __get_selection(self, number_of_threads_in_current_step):
        return np.s_[sum(self.dataset_file_lenght[0:self.current_dataset]):
                     sum(self.dataset_file_lenght[0:self.current_dataset + number_of_threads_in_current_step]), ]

    # Override
    def recommended_chunk_shape(self):
        return None

    # Override
    def recommended_data_shape(self):
        return self.shape

    # Override
    @property
    def dtype(self):
        return np.dtype('float64')

    # Override
    @property
    def maxshape(self):
        return self.shape
