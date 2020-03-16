import fnmatch
import os

from fl.datamigration.tools.dataset import Dataset
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class DataScanner:
    def __init__(self, data_path, animal_name, date=None):
        validate_parameters_not_none(__name__, data_path, animal_name)

        self.data = self.__get_data(data_path, animal_name, date)

    def __get_data(self, data_path, animal_name, date):
        return {animal_name: self.__get_experiments(data_path, animal_name, date)}

    def __get_experiments(self, data_path, animal_name, date):
        preprocessing_path = data_path + animal_name + '/preprocessing'
        if not date:
            dates = sorted(os.listdir(preprocessing_path))
            return {date: self.__get_datasets(preprocessing_path + '/' + date) for date in dates}
        return {date: self.__get_datasets(preprocessing_path + '/' + date)}

    @staticmethod
    def __get_datasets(date_path):
        existing_datasets = set()
        datasets = {}
        directories = os.listdir(date_path)
        directories.sort()

        for directory in directories:
            dir_split = directory.split('_')
            if dir_split[0].isdigit():
                dir_last_part = dir_split.pop().split('.')
                dataset_name = dir_split.pop() + '_' + dir_last_part[0]
                if not (dataset_name in existing_datasets):
                    datasets[dataset_name] = Dataset(dataset_name)
                    existing_datasets.add(dataset_name)
                for dataset in datasets.values():
                    if dataset_name == dataset.name:
                        dataset.add_data_to_dataset(date_path + '/' + directory + '/', dir_last_part.pop())
        return datasets

    def get_all_animals(self):
        return list(self.data.keys())

    def get_all_experiment_dates(self, animal):
        return list(self.data[animal].keys())

    def get_all_datasets(self, animal, date):
        return list(self.data[animal][date].keys())

    def get_metadata(self, animal, date):
        return self.get_experiments(animal)[date]

    def get_mda_timestamps(self, animal, date, dataset):
        for file in self.data[animal][date][dataset].get_all_data_from_dataset('mda'):
            if file.endswith('timestamps.mda'):
                return self.data[animal][date][dataset].get_data_path_from_dataset('mda') + file
        return None

    @staticmethod
    def get_probes_from_directory(path):
        probes = []
        files = os.listdir(path)
        files.sort()
        for probe_file in files:
            if fnmatch.fnmatch(probe_file, "probe*.yml"):
                probes.append(path + '/' + probe_file)
        return probes
