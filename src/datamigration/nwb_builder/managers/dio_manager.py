from src.datamigration.nwb_builder.managers.dio_files import DioFiles


class DioManager:

    def __init__(self, datasets, dio_metadata):
        self.datasets = datasets
        self.dio_metadata = dio_metadata

    def get_dio_files(self):
        multiple_datasets_dio_files = [DioFiles.get_dio_dict(dataset) for dataset in self.datasets]
        filtered_datasets_dio_files = self.__filter_dio_files(multiple_datasets_dio_files)
        return filtered_datasets_dio_files

    def __filter_dio_files(self, multiple_datasets_dio_files):
        metadata_filter = [dio_event['name'] for dio_event in self.dio_metadata]
        filtered__files = [{dio_file: single_dataset[dio_file]
                            for dio_file in single_dataset if dio_file in metadata_filter}
                           for single_dataset in multiple_datasets_dio_files]
        return filtered__files

    def merge_dio_data(self, dio_from_multiple_datasets):
        merged_dio_data = [[] for n in range(len(dio_from_multiple_datasets[0]))]
        for dio_from_single_dataset in dio_from_multiple_datasets:
            for i in range(len(dio_from_single_dataset)):
                merged_dio_data[i] += dio_from_single_dataset[i]
        return merged_dio_data
