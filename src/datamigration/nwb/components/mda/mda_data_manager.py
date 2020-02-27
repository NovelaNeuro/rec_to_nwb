from mountainlab_pytools.mdaio import readmda

from src.datamigration.nwb.common.data_manager import DataManager


class MdaDataManager(DataManager):
    def __init__(self, directories):
        DataManager.__init__(self, directories)

    # override
    def read_data(self, dataset_id, file_id):
        return readmda(self.directories[dataset_id][file_id])

