import logging.config
import os  #

from mountainlab_pytools.mdaio import readmda
from pandas import np
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.managers.abstract_timestamps_data_manager import AbstractTimestampDataManager

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaTimestampDataManager(AbstractTimestampDataManager):
    def __init__(self, directories, continuous_time_directories):
        self.directories = directories
        self.continuous_time_directories = continuous_time_directories

        self.number_of_datasets = self.__get_number_of_datasets()
        self.file_lenghts_in_datasets = self.__get_files_length_in_datasets()

    def __get_number_of_datasets(self):
        return np.shape(self.directories)[1]

    def __get_files_length_in_datasets(self):
        return [self.__get_data_shape(i) for i in range(self.number_of_datasets)]

    @staticmethod
    def __convert_timestamps(continuous_time_dict, converted_timestamps, timestamps):
        for i in range(np.shape(timestamps)[0]):
            key = str(timestamps[i])
            value = continuous_time_dict.get(key, float('nan')) / 1E9

            converted_timestamps[i] = value
            if np.isnan(value):
                message = 'Following key: ' + str(key) + ' does not exist in continioustime dictionary!'
                logger.exception(message)

    def __read_continuous_time(self, dataset_id):
        return readTrodesExtractedDataFile(self.continuous_time_directories[dataset_id])

    @staticmethod
    def __read_timestamps(directories, dataset_id):
        return readmda(directories[0][dataset_id])

    @staticmethod
    def __create_timestamps_array(timestamps):
        return np.ndarray([np.shape(timestamps)[0], ], dtype="float64")

    @staticmethod
    def __create_continuous_time_dict(continuous_time):
        return {str(data[0]): float(data[1]) for data in continuous_time['data']}

    def __get_data_shape(self, dataset_num):
        dim1 = np.shape(self.read_data(dataset_num))[0]
        return dim1

    # override
    def read_data(self, dataset_id):
        timestamps = self.__read_timestamps(self.directories, dataset_id)
        continuous_time = self.__read_continuous_time(dataset_id)
        continuous_time_dict = self.__create_continuous_time_dict(continuous_time)
        converted_timestamps = self.__create_timestamps_array(timestamps)

        self.__convert_timestamps(continuous_time_dict, converted_timestamps, timestamps)

        return converted_timestamps

    # override
    def get_final_data_shape(self):
        return sum(self.file_lenghts_in_datasets),
