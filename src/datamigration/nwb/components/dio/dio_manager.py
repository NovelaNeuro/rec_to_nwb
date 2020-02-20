import concurrent.futures

from pandas import np

from src.datamigration.nwb.components.dio.dio_extractor import DioExtractor


class DioManager:

    def __init__(self, dio_files, dio_metadata, continuous_time_dicts):
        self.dio_files = dio_files
        self.dio_metadata = dio_metadata
        self.continuous_time_dicts = continuous_time_dicts

        self.dio_extractor = DioExtractor()

    def get_dio(self):
        all_dio_data = []
        threads = []
        number_of_datasets = len(self.dio_files)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(number_of_datasets):
                threads.append(executor.submit(self.dio_extractor.extract_dio_for_single_dataset,
                                               self.dio_files[i],
                                               self.continuous_time_dicts[i]))
        for thread in threads:
            all_dio_data.append(thread.result())
        return self.__merge_dio_data(all_dio_data)

    @classmethod
    def __merge_dio_data(cls, data_from_multiple_datasets):
        merged_data = data_from_multiple_datasets[0]
        for single_dataset_data in data_from_multiple_datasets[1:]:
            for event, timeseries in single_dataset_data.items():
                merged_data[event][0] = np.hstack((merged_data[event][0], timeseries[0]))
                merged_data[event][1].extend(timeseries[1])

        return merged_data
