from unittest import TestCase

import numpy as np

from src.datamigration.nwb_builder.iterators.data_iterator_1_dim import DataIterator1D


class TestDataIterator(TestCase):
    def test_data_iterator(self):
        fake_data = FakeTimestampDataManager()
        iterated_data = DataIterator1D(fake_data)

        aaaa = iterated_data
        self.assertEqual(np.shape(aaaa)[0], 11)


class FakeTimestampDataManager:
    def __init__(self):
        self.directories = 0
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
