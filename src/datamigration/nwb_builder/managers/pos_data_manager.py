import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.managers.data_manager_interface import DataManagerInterface


class PosDataManager(DataManagerInterface):
    def __init__(self, directories):
        DataManagerInterface.__init__(self, directories)

    # override
    def read_data(self, dataset_id, file_id):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_id][file_id])
        position = pd.DataFrame(pos_online['data'])
        return position.xloc, position.yloc, position.xloc2, position.yloc2

