import numpy as np
from mountainlab_pytools.mdaio import readmda

class BinaryData:
    def __init__(self, directories):
        self.directories = directories
        self.num_datasets = np.size(directories, 0)
        self.single_dataset_len = np.size(directories, 1)
        self.num_rows_per_file = self.get_data_shape(0)[0]
        self.file_lenghts = [self.get_data_shape(i)[1] for i in range(self.num_datasets)]

    def get_final_data_shape(self):
        return self.num_rows_per_file * self.single_dataset_len, sum(self.file_lenghts)

    def read_data(self, dataset_num, file_num):
        return [0]  # to be overloaded by inheriting classes

    def get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num, 0), 0)
        dim2 = np.size(self.read_data(dataset_num, 0), 1)
        return dim1, dim2


class MdaData(BinaryData):
    def read_data(self, dataset_num, file_num):
        return readmda(self.directories[dataset_num][file_num])


class MdaTimestamps(BinaryData):
    def __init__(self, directories):
        self.directories = directories
        self.num_datasets = np.size(directories, 1)
        print(self.num_datasets)
        print(self.get_data_shape(1))
        self.file_lenghts = [self.get_data_shape(i) for i in range(self.num_datasets)]

    def read_data(self, dataset_num):
        return readmda(self.directories[0][dataset_num])

    def get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num), 0)
        return dim1

    def get_final_data_shape(self):
        return sum(self.file_lenghts),
