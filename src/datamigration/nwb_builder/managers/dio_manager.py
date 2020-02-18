import concurrent.futures

from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.managers.dio_files import DioFiles


class DioManager:

    def __init__(self, directories, dio_metadata, continuous_time_dicts):
        self.dio_metadata = dio_metadata
        self.dio_files = DioFiles(directories, self.dio_metadata)
        self.filtered_dio_files = self.dio_files.get_dio_files()
        self.continuous_time_dicts = continuous_time_dicts
        self.dio_extractor = DioExtractor(self.filtered_dio_files, continuous_time_dicts)

    def get_dio(self):
        all_dio_data = []
        threads = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(len(self.filtered_dio_files)):
                threads.append(executor.submit(self.dio_extractor.extract_dio_for_single_dataset,
                                               self.filtered_dio_files[i],
                                               self.continuous_time_dicts[i]))
        for thread in threads:
            all_dio_data.append(thread.result())
        return self.__merge_dio_data(all_dio_data)

    @classmethod
    def __merge_dio_data(cls, data_from_multiple_datasets):
        merged_data = data_from_multiple_datasets[0]
        for single_dataset_data in data_from_multiple_datasets[1:]:
            for event, timeseries in single_dataset_data.items():
                merged_data[event].extend(timeseries)
        return merged_data
