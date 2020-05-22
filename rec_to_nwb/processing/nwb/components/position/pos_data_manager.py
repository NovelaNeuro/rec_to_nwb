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
        labels = self.get_column_labels(dataset_id, file_id)
        filtered_position = [position[label] for label in labels]
        return filtered_position

    def get_column_labels(self, dataset_id, file_id):
        """extract column labels from POS files"""
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_id][file_id])
        column_labels = pd.DataFrame(pos_online['data']).columns
        column_labels = column_labels[1:]
        column_labels_list = [label for label in column_labels]
        return column_labels_list
