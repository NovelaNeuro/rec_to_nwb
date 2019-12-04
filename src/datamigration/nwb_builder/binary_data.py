import numpy as np


class BinaryData:
    def __init__(self, directories, data_type):
        self.directories = directories
        self.num_datasets = np.size(directories, 0)
        self.num_rows_per_file = self.get_data_shape(0)[0]
        self.data_len = [self.get_data_shape(j, i)[1]
                         for i in np.size(directories, 1) for j in range(self.num_datasets)]
        self.data_type = data_type

    def read_data(self, dataset_num, file_num):
        return  # to be overloaded by inheriting classes

    def get_data_shape(self, num_of_dim):
        return 0  # to be overloaded by inheriting classes
