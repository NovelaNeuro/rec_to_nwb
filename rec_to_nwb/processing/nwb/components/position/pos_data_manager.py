import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from rec_to_nwb.processing.nwb.common.data_manager import DataManager


class PosDataManager(DataManager):
    def __init__(self, directories):
        DataManager.__init__(self, directories)

    # override
    def read_data(self, dataset_id, file_id):
        """extract data from POS files and build FlPos"""

        pos_online = readTrodesExtractedDataFile(self.directories[dataset_id][file_id])
        position = pd.DataFrame(pos_online['data'])
        return position.xloc, position.yloc, position.xloc2, position.yloc2
