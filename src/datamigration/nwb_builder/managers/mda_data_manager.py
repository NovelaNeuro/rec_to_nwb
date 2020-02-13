from mountainlab_pytools.mdaio import readmda

from src.datamigration.nwb_builder.managers.data_manager_interface import DataManagerInterface


class MdaDataManager(DataManagerInterface):
    def __init__(self, directories):
        DataManagerInterface.__init__(self, directories)

    # override
    def read_data(self, dataset_id, file_id):
        return readmda(self.directories[dataset_id][file_id])

