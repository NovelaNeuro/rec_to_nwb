from src.datamigration.nwb_builder.managers.dio_files import DioFiles


class DioManager:

    def __init__(self, directories, dio_metadata):
        self.directories = directories
        self.dio_metadata = dio_metadata

    def get_dio_files(self):
        multiple_datasets_dio_files = [DioFiles.get_dio_dict(dataset) for dataset in self.directories]
        filtered_datasets_dio_files = self.__filter_dio_files(multiple_datasets_dio_files)
        return filtered_datasets_dio_files

    def __filter_dio_files(self, multiple_datasets_dio_files):
        return [{dio_file: single_dataset[dio_file] for dio_file in single_dataset
                 if dio_file in [dio_event['name'] for dio_event in self.dio_metadata]}
                for single_dataset in multiple_datasets_dio_files]

    def merge_dio_data(self, data_from_multiple_datasets):
        merged_data = data_from_multiple_datasets[0]
        for single_dataset_data in data_from_multiple_datasets[1:]:
            for event, timeseries in single_dataset_data.items():
                merged_data[event].extend(timeseries)
        return merged_data
