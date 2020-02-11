from mountainlab_pytools.mdaio import readmda

from src.datamigration.nwb_builder.managers.data_manager_interface import DataManagerInterface


class MdaDataManager(DataManagerInterface):
    def __init__(self, directories):
        self.directories = directories

        # ToDo Think about adding build for this fields
        self.number_of_datasets = self._get_number_of_datasets(directories)
        self.number_of_files_per_dataset = self._get_number_of_files_per_dataset(directories)
        self.number_of_rows_per_file = self._get_data_shape(0)[0]
        self.file_lenghts_in_datasets = self._get_file_length(self.number_of_datasets)

    # override
    def read_data(self, dataset_num, file_num):
        return readmda(self.directories[dataset_num][file_num])

    # override
    def get_final_data_shape(self):
        return self.number_of_rows_per_file * self.number_of_files_per_dataset, sum(self.file_lenghts_in_datasets)
