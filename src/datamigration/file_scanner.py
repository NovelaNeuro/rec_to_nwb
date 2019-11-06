import os


class Directory:
    def __init__(self):
        print('aaa')

    def get_directories(self, path):
        directories = os.listdir(path)


class Data_Directory(Directory):
    def __init__(self, path):
        self.path = path
        self.animal_directories = self.get_animal_directories(self, path)

    def get_animal_directories(self, path):
        animal_directories = os.listdir(path)
        return animal_directories


class Animal_Directory(Directory):
    def __init__(self, path):
        self.path = path
        self.preprocessing_path = path + '/preprocessing'

    def get_date_directories(self):
        date_directories = [directory for directory in os.listdir(self.preprocessing_path) if
                            directory.isnumeric() and len(directory) == 8]  # 8 numbers for date (yyyymmdd)
        return date_directories


class Date_Directory(Directory):
    def __init__(self, path):
        self.path = path
        self.mda_folder = 'aaa'
        self.mda_files = self.get_mda_files(self, path)
        self.mda_timestamp = self.get_mda_timestamp_file(self, path)

    def get_all_directories(self):
        print('aaa')

    def get_mda_files(self):
        mda_files = [mda_file for mda_file in os.listdir(self.path + self.mda_folder) if
                     mda_file.endswith('.mda') and not (mda_file.endswith('timestamp.mda'))]
        return mda_files

    def get_mda_timestamp_file(self, path):
        timestamp_files = [mda_file for mda_file in os.listdir(self.path + self.mda_folder) if
                           mda_file.endswith('timestamp.mda')]
        return timestamp_files

    def split_into_datasets(self):
        print('aaa')

    def get_datasets(self):
        print('aaaa')


class Dataset(Directory):
    def __init__(self):
        print('asd')
