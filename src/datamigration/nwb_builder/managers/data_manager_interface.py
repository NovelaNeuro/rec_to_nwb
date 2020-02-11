import abc

import numpy as np


class DataManagerInterface(abc.ABC):
    @abc.abstractmethod
    def read_data(self, dataset_num, file_num):
        pass

    @abc.abstractmethod
    def get_final_data_shape(self):
        pass

    @staticmethod
    def get_number_of_files_per_dataset(directories):
        return np.shape(directories)[1]

    def _get_data_shape(self, dataset_num):
        dim1 = np.shape(self.read_data(dataset_num, 0))[0]
        dim2 = np.shape(self.read_data(dataset_num, 0))[1]
        return dim1, dim2

    def _get_file_length(self, number_of_datasets):
        return [self._get_data_shape(i)[1] for i in range(number_of_datasets)]

    @staticmethod
    def get_number_of_datasets(directories):
        return np.shape(directories)[0]

    @abc.abstractmethod
    def get_directories(self):
        pass

    @abc.abstractmethod
    def get_number_of_rows_per_file(self):
        pass

    @abc.abstractmethod
    def get_file_lenghts_in_datasets(self):
        pass
