from fl.datamigration.nwb.components.analog.fl_analog_builder import FlAnalogBuilder
from fl.datamigration.nwb.components.analog.fl_analog_extractor import FlAnalogExtractor
from fl.datamigration.validation.equal_length_validator import EqualLengthValidator
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator

import numpy as np


class FlAnalogManager:

    def __init__(self, analog_files, continuous_time_files):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(analog_files))
        validation_registrator.register(NotNoneValidator(continuous_time_files))
        validation_registrator.register(EqualLengthValidator([analog_files, continuous_time_files]))
        validation_registrator.validate()

        self.analog_files = analog_files
        self.continuous_time_files = continuous_time_files

    def get_analog(self):
        """"extract data from analog files"""

        all_analog_data = []
        number_of_datasets = len(self.analog_files)
        for i in range(number_of_datasets):
            all_analog_data.append(
                FlAnalogExtractor.extract_analog_for_single_dataset(
                    self.analog_files[i],
                    self.continuous_time_files[i]
                )
            )
        merged_epochs = self.__merge_epochs(all_analog_data)
        analog_data = self.__merge_analog_sensors(merged_epochs)
        return FlAnalogBuilder.build(analog_data, self.__get_timestamps(merged_epochs))

    @staticmethod
    def __merge_epochs(data_from_multiple_datasets):
        merged_epochs = data_from_multiple_datasets[0]
        for single_dataset_data in data_from_multiple_datasets[1:]:
            for analog_file in single_dataset_data.keys():
                merged_epochs[analog_file] = np.hstack((merged_epochs[analog_file], single_dataset_data[analog_file]))
        return merged_epochs

    @classmethod
    def __merge_analog_sensors(cls, merged_epochs):
        analog_sensors = [merged_epochs[analog_sensor] for analog_sensor in merged_epochs.keys() if 'timestamp' not in analog_sensor]
        merged_analog_sensors = np.array(analog_sensors, np.int32)
        transposed_analog_data = np.ndarray.transpose(merged_analog_sensors)
        return transposed_analog_data

    @classmethod
    def __get_timestamps(cls, merged_epochs):
        for analog_sensor in merged_epochs.keys():
            if 'timestamps' in analog_sensor:
                return merged_epochs[analog_sensor]



