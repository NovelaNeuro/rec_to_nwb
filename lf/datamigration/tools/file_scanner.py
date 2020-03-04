import fnmatch
import os


class Dataset:
    def __init__(self, name):
        self.name = name
        self.data = dict([])

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


class DataScanner:
    def __init__(self, animal_name, path):
        self.anima_name = animal_name
        self.path = path
        self.data = self.get_data()

    @staticmethod
    def get_datasets(path):
        existing_datasets = set()
        datasets = dict([])
        directories = os.listdir(path)
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
                        dataset.add_data_to_dataset(path + '/' + directory + '/', dir_last_part.pop())
        return datasets

    def get_data(self):
        return self.get_experiments(self.animal_name)

    def get_experiments(self, animal_name):
        path = self.path + animal_name + '/preprocessing'
        dates = sorted(os.listdir(path))
        experiment_dates = dict([])
        for date in dates:
            experiment_dates[date] = self.get_datasets(path + '/' + date)
        return experiment_dates

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
