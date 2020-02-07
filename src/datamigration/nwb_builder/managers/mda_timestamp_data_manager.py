import logging.config
import os  #

from mountainlab_pytools.mdaio import readmda
from pandas import np
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaTimestampDataManager():
    def __init__(self, directories, continuous_time_directories):
        self.directories = directories
        self.continuous_time_directories = continuous_time_directories

        self.continuous_time_dict = {}
        self.number_of_datasets = self._get_number_of_datasets()
        self.files_lengths_in_dataset = self._get_files_length_in_datasets()

    def read_data(self, dataset_id):
        timestamps = self._read_timestamps(dataset_id)
        continuous_time = self._read_continuous_time(dataset_id)
        continuous_time_dict = self._create_continuous_time_dict(continuous_time)
        converted_timestamps = self._create_timestamps_array(timestamps)

        self._convert_timestamps(continuous_time_dict, converted_timestamps, timestamps)

        return converted_timestamps

    def get_final_data_shape(self):
        return sum(self.files_lengths_in_dataset),

    def _get_number_of_datasets(self):
        return np.size(self.directories, 1)

    def _get_files_length_in_datasets(self):
        return [self._get_data_shape(i) for i in range(self.number_of_datasets)]

    @staticmethod
    def _convert_timestamps(continuous_time_dict, converted_timestamps, timestamps):
        for i in range(np.shape(timestamps)[0]):
            key = str(timestamps[i])
            value = continuous_time_dict.get(key, float('nan')) / 1E9

            converted_timestamps[i] = value
            if np.isnan(value):
                message = 'Following key: ' + str(key) + ' does not exist in continioustime dictionary!'
                logger.exception(message)

    def _read_continuous_time(self, dataset_id):
        return readTrodesExtractedDataFile(self.continuous_time_directories[dataset_id])

    def _read_timestamps(self, dataset_id):
        return readmda(self.directories[0][dataset_id])

    @staticmethod
    def _create_timestamps_array(timestamps):
        return np.ndarray([np.size(timestamps, 0), ], dtype="float64")

    @staticmethod
    def _create_continuous_time_dict(continuous_time):
        return {str(data[0]): float(data[1]) for data in continuous_time['data']}

    def _get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num), 0)
        return dim1


