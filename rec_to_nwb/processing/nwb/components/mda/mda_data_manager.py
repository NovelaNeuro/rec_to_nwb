from mountainlab_pytools.mdaio import DiskReadMda, readmda
from numpy import isclose
from rec_to_nwb.processing.nwb.common.data_manager import DataManager


class MdaDataManager(DataManager):
    def __init__(self, directories, raw_to_uv):
        self.raw_to_uv = raw_to_uv
        DataManager.__init__(self, directories)
    # override

    def read_data(self, dataset_id, file_id):
        # read the data from the MDA file, convert to uV and then return as int16 unless the data are already in uV
        if not isclose(self.raw_to_uv, 1.0):
            return (readmda(self.directories[dataset_id][file_id]) * self.raw_to_uv).astype('int16')
        else:
            return readmda(self.directories[dataset_id][file_id]).astype('int16')

    # override to make more efficient
    def _get_data_shape(self, dataset_id, file_num=0):
        # use DiskReadMDA to return a two element list with the MxN data dimensions for the first file in a given dataset
        return DiskReadMda(self.directories[dataset_id][file_num]).dims()

    # override to make more efficient; not clear if this is used right now.
    def _get_number_of_rows_per_file(self):
        dataset_num = 0   # assume that all datasets have identical structures
        # all files may not have the same numbers of rows (e.g. channels)
        return [self.get_data_shape(dataset_num, file_num)[0]
                for file_num in range(self.number_of_files_per_dataset)]
