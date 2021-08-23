import os


class DioFiles:

    def __init__(self, directories, dio_metadata):
        self.directories = directories
        self.dio_metadata = dio_metadata

    def get_files(self):
        multiple_datasets_dio_files = [self.__get_dict(
            dataset) for dataset in self.directories]
        filtered_datasets_dio_files = self.__filter_files(
            multiple_datasets_dio_files, self.dio_metadata)
        return filtered_datasets_dio_files

    @classmethod
    def __filter_files(cls, multiple_datasets_dio_files, dio_metadata):
        return [{dio_file: single_dataset[dio_file] for dio_file in single_dataset
                 if dio_file in [dio_event['description'] for dio_event in dio_metadata]}
                for single_dataset in multiple_datasets_dio_files]

    @classmethod
    def __get_dict(cls, directory):
        dio_dict = {}
        files = os.listdir(directory)
        files.sort()
        for file in files:
            if file.endswith('.dat'):
                split_filename = file.split('.')
                dio_dict[split_filename[-2].split('_')
                         [1]] = directory + '/' + file
        return dio_dict
