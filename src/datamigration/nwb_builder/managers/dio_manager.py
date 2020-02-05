import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class DioManager:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_behavioral_events(self):
        all_dio_timeseries = self.metadata['behavioral_events']
        return all_dio_timeseries

    def get_dio_dict(self, directory):
        dio_dict = {}
        for file in os.listdir(directory):
            if (file.endswith('.dat')):
                split_filename = file.split('.')
                dio_dict[split_filename[-2].split('_')[1]] = file
        return dio_dict

    def get_single_extracted_dio(self, dataset, name):
        dio_set = dataset.get_all_data_from_dataset('DIO')
        dio_path = dataset.get_data_path_from_dataset('DIO')
        for dio_file in dio_set:
            if name + '.' in dio_file:
                dio_data = readTrodesExtractedDataFile(dio_path + dio_file)
                return dio_data
        return None
