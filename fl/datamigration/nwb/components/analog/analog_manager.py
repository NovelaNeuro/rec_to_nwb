import concurrent.futures

import numpy as np

from fl.datamigration.nwb.components.analog.analog_extractor import AnalogExtractor


class AnalogManager:

    def __init__(self, analog_files, continuous_time_files):
        self.analog_files = analog_files
        self.continuous_time_files = continuous_time_files

    def get_analog(self):
        """"extract data from DIO files and match them with metadata"""

        all_analog_data = []
        number_of_datasets = len(self.analog_files)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(number_of_datasets):
                all_analog_data.append(AnalogExtractor.extract_analog_for_single_dataset(self.analog_files[i],
                                                                                self.continuous_time_files[i]))
        return self.__merge_analog_data(all_analog_data)

    @classmethod
    def __merge_analog_data(cls, data_from_multiple_datasets):
        merged_data = data_from_multiple_datasets[0]
        for single_dataset_data in data_from_multiple_datasets[1:]:
            for event, timeseries in single_dataset_data.items():
                merged_data[event][0] = np.hstack((merged_data[event][0], timeseries[0]))
                merged_data[event][1].extend(timeseries[1])

        return merged_data
