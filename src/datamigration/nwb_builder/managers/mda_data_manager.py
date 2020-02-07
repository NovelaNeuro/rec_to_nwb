from mountainlab_pytools.mdaio import readmda
from pandas import np


class MdaDataManager:
    def __init__(self, directories):
        self.directories = directories

        # ToDo Think about adding build for this fields
        self.number_of_datasets = self._get_number_of_datasets(directories)
        self.number_of_files_per_dataset = self._get_number_of_files_per_dataset(directories)
        self.number_of_rows_per_file = self._get_data_shape(0)[0]
        self.files_lengths_in_dataset = self._get_file_length()

    @staticmethod
    def _get_number_of_datasets(directories):
        return np.size(directories, 0)

    @staticmethod
    def _get_number_of_files_per_dataset(directories):
        return np.size(directories, 1)

    def _get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num, 0), 0)
        dim2 = np.size(self.read_data(dataset_num, 0), 1)
        return dim1, dim2

    def _get_file_length(self):
        return [self._get_data_shape(i)[1] for i in range(self.number_of_datasets)]

    def read_data(self, dataset_num, file_num):
        return readmda(self.directories[dataset_num][file_num])

    def get_final_data_shape(self):
        return self.number_of_rows_per_file * self.number_of_files_per_dataset, sum(self.files_lengths_in_dataset)
