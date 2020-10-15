import numpy as np

from rec_to_nwb.processing.nwb.components.dio.old_dio_extractor import OldDioExtractor


class OldDioManager:

    def __init__(self, dio_files, dio_metadata):
        self.dio_files = dio_files
        self.dio_metadata = dio_metadata

    def get_dio(self):
        """"extract data from DIO files and match them with metadata"""

        all_dio_data = []
        number_of_datasets = len(self.dio_files)
        for i in range(number_of_datasets):
            all_dio_data.append(
                OldDioExtractor.extract_dio_for_single_dataset(
                    filtered_files=self.dio_files[i]
                )
            )
        return self.__merge_dio_data(all_dio_data)

    @classmethod
    def __merge_dio_data(cls, data_from_multiple_datasets):
        merged_data = data_from_multiple_datasets[0]
        for single_dataset_data in data_from_multiple_datasets[1:]:
            for event, timeseries in single_dataset_data.items():
                merged_data[event][0] = np.hstack((merged_data[event][0], timeseries[0]))
                merged_data[event][1].extend(timeseries[1])

        return merged_data
