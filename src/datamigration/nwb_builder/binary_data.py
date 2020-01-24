from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from mountainlab_pytools.mdaio import readmda
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


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


class MdaData(BinaryData):

    def read_data(self, dataset_num, file_num):
        return readmda(self.directories[dataset_num][file_num])


class PosData(BinaryData):

    def read_data(self, dataset_num, file_num):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_num][file_num])
        position = pd.DataFrame(pos_online['data'])
        return position.xloc, position.yloc, position.xloc2, position.yloc2


class BinaryData1D(ABC):
    def __init__(self, directories):
        self.directories = directories
        self.num_datasets = self.get_num_datasets()
        self.file_lenghts = [self.get_data_shape(i) for i in range(self.num_datasets)]

    @abstractmethod
    def get_num_datasets(self):
        pass

    @abstractmethod
    def read_data(self, dataset_num, file_num=0):
        pass

    @abstractmethod
    def get_data_shape(self, dataset_num):
        pass

    @abstractmethod
    def get_final_data_shape(self):
        pass


class MdaTimestamps(ABC):
    def __init__(self, directories, continuous_time_directories):
        self.cont_time_dict = {}
        self.directories = directories
        self.countinuous_time_directories = continuous_time_directories
        self.num_datasets = self.get_num_datasets()
        self.file_lenghts = [self.get_data_shape(i) for i in range(self.num_datasets)]


    def get_num_datasets(self):
        return np.size(self.directories, 1)

    def read_data(self, dataset_num, file_num=0):
        timestamps = readmda(self.directories[0][dataset_num])
        data_float = np.ndarray([np.size(timestamps, 0), ], dtype="float64")
        continuous_time = readTrodesExtractedDataFile(self.countinuous_time_directories[0][dataset_num])
        continuous_time_dict = {}
        for data in continuous_time['data']:
            continuous_time_dict[str(data[0])] = float(data[1])
        for i in range(np.shape(timestamps)[0]):
            if not timestamps[i] == 0:
                data_float[i] = float(continuous_time_dict[str(timestamps[i])]) / 1E9
            else:
                data_float[i] = 0.0
        return data_float

    def get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num), 0)
        return dim1

    def get_final_data_shape(self):
        return sum(self.file_lenghts),


class PosTimestamps(BinaryData1D):

    def get_num_datasets(self):
        return np.size(self.directories, 0)

    def read_data(self, dataset_num, file_num=0):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_num][0])
        position = pd.DataFrame(pos_online['data'])
        timestamps = position.time.to_numpy()
        for i in range(np.size(timestamps, 0)):
            timestamps[i] = timestamps[i] / 1000
        return timestamps

    def get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num), 0)
        return dim1

    def get_final_data_shape(self):
        return sum(self.file_lenghts),
