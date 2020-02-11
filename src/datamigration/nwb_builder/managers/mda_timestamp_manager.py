import logging.config
import os  #

from mountainlab_pytools.mdaio import readmda
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.managers.timestamps_manager_interface import TimestampManagerInterface

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaTimestampDataManager(TimestampManagerInterface):
    def __init__(self, directories, continuous_time_directories):
        self.directories = directories
        self.continuous_time_directories = continuous_time_directories

        self.number_of_datasets = self._get_number_of_datasets(self.directories)
        self.file_lenghts_in_datasets = self._get_file_lenghts_in_datasets()

    # override
    def _get_timestamps(self, dataset_id):
        return readmda(self.directories[0][dataset_id])

    # override
    def _get_continuous_time_dict(self, dataset_num):
        continuous_time = readTrodesExtractedDataFile(self.continuous_time_directories[dataset_num])
        continuous_time_dict = {str(data[0]): float(data[1]) for data in continuous_time['data']}
        return continuous_time_dict

    # override
    def _get_file_lenghts_in_datasets(self):
        return [self._get_data_shape(i) for i in range(self.number_of_datasets)]

    # override
    @staticmethod
    def _read_timestamps(directories, dataset_id):
        return readmda(directories[0][dataset_id])

    # override
    def read_data(self, dataset_id):
        timestamps = self._read_timestamps(self.directories, dataset_id)
        continuous_time_dict = self._get_continuous_time_dict(dataset_id)
        converted_timestamps = self._convert_timestamps(continuous_time_dict, timestamps)

        return converted_timestamps

    # override
    def get_final_data_shape(self):
        return sum(self.file_lenghts_in_datasets),

    # override
    def get_directories(self):
        return self.directories

    # override
    def get_number_of_datasets(self):
        return self.number_of_datasets

    # override
    def get_file_lenghts_in_datasets(self):
        return self.file_lenghts_in_datasets
