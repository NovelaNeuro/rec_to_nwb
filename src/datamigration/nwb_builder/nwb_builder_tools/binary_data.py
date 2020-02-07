import logging.config
import os

import numpy as np
import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)



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
