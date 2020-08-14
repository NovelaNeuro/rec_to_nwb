from mountainlab_pytools.mdaio import readmda

from rec_to_nwb.processing.nwb.common.data_manager import DataManager


class MdaDataManager(DataManager):
    def __init__(self, directories, conversion):
        self.conversion = conversion
        DataManager.__init__(self, directories)

    # override
    def read_data(self, dataset_id, file_id):
        data = readmda(self.directories[dataset_id][file_id])
        return data * float(self.conversion)
