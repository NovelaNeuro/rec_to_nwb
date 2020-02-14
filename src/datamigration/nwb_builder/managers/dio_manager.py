from src.datamigration.nwb_builder.managers.dio_files import DioFiles


class DioManager:

    def __init__(self, datasets, dio_metadata):
        self.datasets = datasets
        self.dio_metadata = dio_metadata

    def get_dio_files(self):
        datasets_dio_files = [DioFiles.get_dio_dict(dataset) for dataset in self.datasets]
        filtered_datasets_dio_files = self.__filter_dio_files(datasets_dio_files, self.dio_metadata)
        return datasets_dio_files

    def __filter_dio_files(self, datasets_dio_files, metadata):
        for dio_files in datasets_dio_files:
            for dio_file in dio_files:
                if
        return filtered_dio_files

    def __merge_dio_data(self, all_datasets_dio_data):
        return merged_dio_data
