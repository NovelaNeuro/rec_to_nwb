from unittest import TestCase

import numpy as np

from fl.processing.nwb.components.iterator.single_thread_timestamp_iterator import SingleThreadTimestampIterator


class TestDataIterator(TestCase):
    def test_data_iterator(self):
        fake_data_manager = FakeTimestampDataManager()
        iterated_data = SingleThreadTimestampIterator(fake_data_manager)
        self.assertEqual((11,), np.shape(iterated_data))

class FakeTimestampDataManager:
    def __init__(self):
        self.number_of_datasets = 2
        self.file_lenghts_in_datasets = [5, 6]
        self.fake_timestamps = [np.ndarray(dtype="float64", shape=[5, ]), np.ndarray(dtype="float64", shape=[6, ])]
        for i in range(2):
            for j in range(len(self.fake_timestamps[i])):
                self.fake_timestamps[i][j] = j

    def read_data(self, dataset_num):
        return self.fake_timestamps[dataset_num]

    def get_final_data_shape(self):
        return 11,

    def get_number_of_datasets(self):
        return self.number_of_datasets

    def get_file_lenghts_in_datasets(self):
        return self.file_lenghts_in_datasets
