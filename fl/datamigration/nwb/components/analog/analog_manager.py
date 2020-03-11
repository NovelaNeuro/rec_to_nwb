import concurrent.futures

import numpy as np

from fl.datamigration.nwb.components.analog.analog_extractor import AnalogExtractor


class AnalogManager:

    def __init__(self, analog_files):
        self.analog_files = analog_files

    def get_analog(self):
        """"extract data from analog files"""

        all_analog_data = []
        number_of_datasets = len(self.analog_files)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(number_of_datasets):
                all_analog_data.append(AnalogExtractor.extract_analog_for_single_dataset(self.analog_files[i]))
        merged_data = self.__merge_analog_data(all_analog_data)
        return self.__stack_analog_data(merged_data), self.__get_timestamps(merged_data)

    @classmethod
    def __merge_analog_data(cls, data_from_multiple_datasets):
        merged_data = data_from_multiple_datasets[0]
        for single_dataset_data in data_from_multiple_datasets[1:]:
            for analog_file in single_dataset_data.keys():
                merged_data[analog_file] = np.hstack((merged_data[analog_file], single_dataset_data[analog_file]))
        return merged_data

    @classmethod
    def __stack_analog_data(cls, merged_data):
        analog_sensors = [merged_data[analog_sensor] for analog_sensor in merged_data.keys() if 'timestamp' not in analog_sensor]
        stacked_analog_sensors = np.vstack(analog_sensors)
        return stacked_analog_sensors

    @classmethod
    def __get_timestamps(cls, merged_data):
        for analog_sensor in merged_data.keys():
            if 'timestamps' in analog_sensor:
                return merged_data[analog_sensor]



