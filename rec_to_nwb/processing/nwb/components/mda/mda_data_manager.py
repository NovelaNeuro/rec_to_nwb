from mountainlab_pytools.mdaio import readmda

from numpy import isclose
from rec_to_nwb.processing.nwb.common.data_manager import DataManager


class MdaDataManager(DataManager):
    def __init__(self, directories, raw_to_uv):
        self.raw_to_uv = raw_to_uv
        DataManager.__init__(self, directories)
    # override
    def read_data(self, dataset_id, file_id):
        # read the data from the MDA file, convert to uV and then return as int16 unless the data are already in uV
        if not isclose(self.raw_to_uv,1.0):
            return (readmda(self.directories[dataset_id][file_id]) * self.raw_to_uv).astype('int16')
        else:
            return readmda(self.directories[dataset_id][file_id]).astype('int16')
