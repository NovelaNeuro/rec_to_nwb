import numpy as np
from mountainlab_pytools.mdaio import readmda

class BinaryData:
    def __init__(self, directories):
        self.directories = directories
        self.num_datasets = np.size(directories, 0)
        self.single_dataset_len = np.size(directories, 1)
        self.num_rows_per_file = self.get_data_shape(0)[0]
        self.file_lenghts = [self.get_data_shape(i)[1] for i in range(self.num_datasets)]

    def get_final_data_shape(self):
        return [self.num_rows_per_file * self.single_dataset_len, sum(self.file_lenghts)]


    def read_data(self, dataset_num, file_num):
        return [0]  # to be overloaded by inheriting classes

    def get_data_shape(self, dataset_num):
        dim1 = np.size(self.read_data(dataset_num, 0), 0)
        dim2 = np.size(self.read_data(dataset_num, 0), 1)
        return dim1, dim2


class MdaData(BinaryData):
    def read_data(self, dataset_num, file_num):
        return readmda(self.directories[dataset_num][file_num])


if __name__ == "__main__":
    path = 'C:/Users/wbodo/Documents/GitHub/LorenFranksDataMigration/src/test/datamigration/res/'
    directories = []
    dataset1 = []
    dataset2 = []
    for i in range(1, 4):
        dataset1.append(path + '20190718_beans_01_s1.nt' + str(i) + '.mda')
        dataset2.append(path + '20190718_beans_01_s1.nt' + str(i) + '.mda')
    directories.append(dataset1)
    directories.append(dataset2)
    mdadata = MdaData(directories)
    print(mdadata.get_final_data_shape())
