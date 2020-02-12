from unittest import TestCase

import numpy as np

from src.datamigration.nwb_builder.iterators.data_iterator_2_dim import DataIterator2D


class TestDataIterator(TestCase):
    def test_data_iterator(self):
        fake_data = FakeDataManager()
        iterated_data = DataIterator2D(fake_data)
        self.assertEqual([11, 8], np.shape(iterated_data))


class FakeDataManager:
    def __init__(self):
        self.number_of_datasets = 2
        self.file_lenghts_in_datasets = [5, 6]
        self.number_of_files_per_dataset = 2
        self.number_of_rows_per_file = 4
        self.fake_timestamps = [np.ndarray(dtype="float64", shape=[4, 5]), np.ndarray(dtype="float64", shape=[4, 6])]
        for i in range(2):
            for j in range(len(self.fake_timestamps[i])):
                for k in range(4):
                    self.fake_timestamps[i][k][j] = j

    def read_data(self, dataset_num, current_file):
        return self.fake_timestamps[dataset_num]

    def get_final_data_shape(self):
        return 8, 11
