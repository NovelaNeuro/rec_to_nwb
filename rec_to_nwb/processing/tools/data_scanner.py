import fnmatch
import os

from rec_to_nwb.processing.exceptions.missing_data_exception import \
    MissingDataException
from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.dataset import Dataset
from rec_to_nwb.processing.tools.file_sorter import FileSorter


class DataScanner:

    @beartype
    def __init__(self, data_path: str, animal_name: str, nwb_metadata: MetadataManager):

        self.data_path = data_path
        self.animal_name = animal_name
        self.nwb_metadata = nwb_metadata

        self.data = None

    @beartype
    def get_all_epochs(self, date: str) -> list:
        epoch_number_to_epoch = {}
        directories = os.listdir(
            os.path.join(
                self.data_path, self.animal_name, 'preprocessing', date))
        FileSorter.sort_filenames(directories)
        for directory in directories:
            if directory.startswith(date):
                epoch_number = directory.split('_')[2]
                epoch_tag = directory.split('_')[3].split('.')[0]
                epoch = f'{epoch_number}_{epoch_tag}'

                if epoch_number in epoch_number_to_epoch:
                    # check if the current epoch_tag is consistent
                    warning = f'epoch {epoch_number} is not consistent across files'
                    assert epoch_number_to_epoch[epoch_number] == epoch, warning
                else:
                    epoch_number_to_epoch[epoch_number] = epoch

        return [epoch_number_to_epoch[epoch_number]
                for epoch_number in sorted(epoch_number_to_epoch)]

    @beartype
    def get_all_data_from_dataset(self, date: str) -> list:
        path = os.path.join(self.data_path, self.animal_name, 'preprocessing',
                            date)
        self.__check_if_path_exists(path)
        return os.listdir(path)

    @beartype
    def extract_data_from_date_folder(self, date: str):
        self.data = {self.animal_name: self.__extract_experiments(
            self.data_path, self.animal_name, [date])}

    @beartype
    def extract_data_from_dates_folders(self, dates: list):
        self.data = {self.animal_name: self.__extract_experiments(
            self.data_path, self.animal_name, dates)}

    def extract_data_from_all_dates_folders(self):
        self.data = {self.animal_name: self.__extract_experiments(
            self.data_path, self.animal_name, None)}

    def __extract_experiments(self, data_path, animal_name, dates):
        preprocessing_path = os.path.join(
            data_path, animal_name, 'preprocessing')
        if not dates:
            dates = FileSorter.sort_filenames(os.listdir(preprocessing_path))
        return {date: self.__extract_datasets(
                os.path.join(preprocessing_path, date)) for date in dates}

    @staticmethod
    def __extract_datasets(date_path):
        existing_datasets = set()
        datasets = {}
        directories = FileSorter.sort_filenames(os.listdir(date_path))

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
                        dataset.add_data_to_dataset(
                            os.path.join(date_path, directory),
                            dir_last_part.pop())
        return datasets

    @beartype
    def get_all_animals(self) -> list:
        return list(self.data.keys())

    @beartype
    def get_all_experiment_dates(self, animal: str) -> list:
        return list(self.data[animal].keys())

    @beartype
    def get_all_datasets(self, animal: str, date: str) -> list:
        return list(self.data[animal][date].keys())

    @beartype
    def get_mda_timestamps(self, animal: str, date: str, dataset: str):
        for file in self.data[animal][date][dataset].get_all_data_from_dataset('mda'):
            if file.endswith('timestamps.mda'):
                return os.path.join(
                    self.data[animal][date][dataset]
                    .get_data_path_from_dataset('mda'), file)

    @staticmethod
    @beartype
    def get_probes_from_directory(path: str):
        probes = []
        files = FileSorter.sort_filenames(os.listdir(path))
        for probe_file in files:
            if fnmatch.fnmatch(probe_file, "probe*.yml"):
                probes.append(os.path.join(path, probe_file))
        return probes

    def __check_if_path_exists(self, path):
        if not os.path.exists(path):
            raise MissingDataException(
                'missing ' + self.data_path + ' directory')
