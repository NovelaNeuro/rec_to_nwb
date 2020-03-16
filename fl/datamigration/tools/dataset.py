import os


class Dataset:
    def __init__(self, name):
        self.name = name
        self.data = {}

    def add_data_to_dataset(self, folder_path, data_type):
        self.data[data_type] = folder_path

    def get_data_path_from_dataset(self, data_type):
        return self.data[data_type]

    def get_all_data_from_dataset(self, data_type):
        directories = os.listdir(self.data[data_type])
        directories.sort()
        return directories

    def get_mda_timestamps(self):
        for file in self.get_all_data_from_dataset('mda'):
            if file.endswith('timestamps.mda'):
                return self.get_data_path_from_dataset('mda') + file
        return None

    def get_continuous_time(self):
        for file in self.get_all_data_from_dataset('time'):
            if file.endswith('continuoustime.dat'):
                return self.get_data_path_from_dataset('time') + file
        return None