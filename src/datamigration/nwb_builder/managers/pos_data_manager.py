import pandas as pd
from pandas import np
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.managers.data_manager import DataManager


class PosDataManager(DataManager):
    def __init__(self, directories):
        self.directories = directories

        # ToDo Think about adding build for this fields
        self.number_of_datasets = self.__get_number_of_datasets(directories)
        self.number_of_files_per_dataset = self.__get_number_of_files_per_dataset(directories)
        self.number_of_rows_per_file = self.__get_data_shape(0)[0]
        self.file_lenghts_in_datasets = self.__get_file_length()

    @staticmethod
    def __get_number_of_datasets(directories):
        return np.size(directories, 0)

    @staticmethod
    def __get_number_of_files_per_dataset(directories):
        return np.size(directories, 1)

    def __get_data_shape(self, dataset_id):
        dim1 = np.size(self.read_data(dataset_id, 0), 0)
        dim2 = np.size(self.read_data(dataset_id, 0), 1)
        return dim1, dim2

    def __get_file_length(self):
        return [self.__get_data_shape(i)[1] for i in range(self.number_of_datasets)]

    # override
    def read_data(self, dataset_id, file_id):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_id][file_id])
        position = pd.DataFrame(pos_online['data'])
        return position.xloc, position.yloc, position.xloc2, position.yloc2

    # override
    def get_final_data_shape(self):
        return self.number_of_rows_per_file * self.number_of_files_per_dataset, sum(self.file_lenghts_in_datasets)
