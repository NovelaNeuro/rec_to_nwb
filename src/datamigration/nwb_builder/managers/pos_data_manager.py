import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.managers.data_manager_interface import DataManagerInterface


class PosDataManager(DataManagerInterface):
    def __init__(self, directories):
        self.directories = directories

        # ToDo Think about adding build for this fields
        self.number_of_datasets = self.get_number_of_datasets(directories)
        self.number_of_files_per_dataset = self.get_number_of_files_per_dataset(directories)
        self.number_of_rows_per_file = self._get_data_shape(0)[0]
        self.file_lenghts_in_datasets = self._get_file_length(self.number_of_datasets)

    # override
    def read_data(self, dataset_id, file_id):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_id][file_id])
        position = pd.DataFrame(pos_online['data'])
        return position.xloc, position.yloc, position.xloc2, position.yloc2

    # override
    def get_final_data_shape(self):
        return self.number_of_rows_per_file * self.number_of_files_per_dataset, sum(self.file_lenghts_in_datasets)

    # override
    def get_directories(self):
        return self.directories

    # override
    def get_number_of_rows_per_file(self):
        return self.number_of_rows_per_file

    # override
    def get_file_lenghts_in_datasets(self):
        return self.file_lenghts_in_datasets
