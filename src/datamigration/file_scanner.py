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
        return os.listdir(self.data[data_type])


class DataScanner:
    def __init__(self, path):
        self.path = path
        self.data = self.get_data()

    def get_data(self):
        animal_names = os.listdir(self.path)
        animals = dict([])
        for animal_name in animal_names:
            animals[animal_name] = self.get_experiments(animal_name)
        return animals

    def get_experiments(self, animal_name):
        path = self.path + animal_name + '/preprocessing'
        dates = os.listdir(path)
        experiment_dates = dict([])
        for date in dates:
            experiment_dates[date] = self.get_datasets(path + '/' + date)
        return experiment_dates

    def get_datasets(self, path):
        existing_datasets = set()
        datasets = dict([])
        directories = os.listdir(path)
        for dir in directories:
            dir_split = dir.split('_')
            dir_last_part = dir_split.pop().split('.')
            dataset_name = dir_split.pop() + '_' + dir_last_part[0]
            if not (dataset_name in existing_datasets):
                datasets[dataset_name] = Dataset(dataset_name)
                existing_datasets.add(dataset_name)
            for dataset in datasets.values():
                if dataset_name == dataset.name:
                    dataset.add_data_to_dataset(path + '/' + dir, dir_last_part.pop())
        return datasets
