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
        labels = self.get_column_labels()
        filtered_position = [position[label] for label in labels]
        return filtered_position

    def get_column_labels(self):
        """extract column labels from POS files"""
        pos_online = readTrodesExtractedDataFile(self.directories[0][0])
        column_labels = pd.DataFrame(pos_online['data']).columns
        column_labels = column_labels[1:]
        column_labels_list = column_labels.values.tolist()
        return column_labels_list

    def get_column_labels_as_string(self):
        """extract column labels from POS files and converts them do single string"""
        labels = self.get_column_labels()
        labels_string = ''
        for label in labels:
            labels_string += label
            if not label == labels[-1]:
                labels_string += ', '
        return labels_string
