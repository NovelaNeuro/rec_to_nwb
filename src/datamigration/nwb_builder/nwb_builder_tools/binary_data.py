import logging.config
import os

import numpy as np
import pandas as pd
from mountainlab_pytools.mdaio import readmda
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


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
        pass

    def get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num, 0), 0)
        dim2 = np.size(self.read_data(dataset_num, 0), 1)
        return dim1, dim2



class PosData(BinaryData):

    def read_data(self, dataset_num, file_num):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_num][file_num])
        position = pd.DataFrame(pos_online['data'])
        return position.xloc, position.yloc, position.xloc2, position.yloc2


class MdaTimestamps():
    def __init__(self, directories, continuous_time_directories):
        self.cont_time_dict = {}
        self.directories = directories
        self.continuous_time_directories = continuous_time_directories
        self.num_datasets = self.get_num_datasets()
        self.file_lenghts = [self.get_data_shape(i) for i in range(self.num_datasets)]

    def get_num_datasets(self):
        return np.size(self.directories, 1)

    def read_data(self, dataset_num):
        timestamps = readmda(self.directories[0][dataset_num])
        timestamps64 = np.ndarray([np.size(timestamps, 0), ], dtype="int64")
        for i in range(np.shape(timestamps)[0]):
            timestamps64[i] = timestamps[i]
        data_float = np.ndarray([np.size(timestamps, 0), ], dtype="float64")
        continuous_time = readTrodesExtractedDataFile(self.continuous_time_directories[dataset_num])
        continuous_time_dict = {str(data[0]): float(data[1]) for data in continuous_time['data']}
        for i in range(np.shape(timestamps)[0]):
            key = str(timestamps[i])
            value = continuous_time_dict.get(key, float('nan')) / 1E9
            data_float[i] = value
            if np.isnan(value):
                message = 'Following key: ' + str(key) + ' does not exist in continioustime dictionary!'
                logger.exception(message)
        return data_float

    def get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num), 0)
        return dim1

    def get_final_data_shape(self):
        return sum(self.file_lenghts),


class PosTimestamps():
    def __init__(self, directories, continuous_time_directories):
        self.directories = directories
        self.continuous_time_directories = continuous_time_directories
        self.num_datasets = self.get_num_datasets()
        self.file_lenghts = [self.get_data_shape(i) for i in range(self.num_datasets)]

    def get_num_datasets(self):
        return np.size(self.directories, 0)

    def read_data(self, dataset_num):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_num][0])
        position = pd.DataFrame(pos_online['data'])
        timestamps = position.time.to_numpy(dtype='int64')
        data_float = np.ndarray([np.size(timestamps, 0), ], dtype="float64")
        continuous_time = readTrodesExtractedDataFile(self.continuous_time_directories[dataset_num])
        continuous_time_dict = {str(data[0]): float(data[1]) for data in continuous_time['data']}
        for i in range(np.shape(timestamps)[0]):
            key = str(timestamps[i])
            try:
                value = continuous_time_dict[key]
                data_float[i] = float(value) / 1E9
            except KeyError as error:
                message = 'Following key: ' + str(key) + ' does not exist!' + str(error)
                logger.exception(message)
                data_float[i] = float('nan')
        return data_float

    def get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num), 0)
        return dim1

    def get_final_data_shape(self):
        return sum(self.file_lenghts),
