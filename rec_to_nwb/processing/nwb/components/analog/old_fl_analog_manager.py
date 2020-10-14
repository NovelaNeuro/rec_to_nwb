import numpy as np

from rec_to_nwb.processing.nwb.components.analog.fl_analog import FlAnalog
from rec_to_nwb.processing.nwb.components.analog.old_fl_analog_builder import OldFlAnalogBuilder
from rec_to_nwb.processing.nwb.components.analog.old_fl_analog_extractor import OldFlAnalogExtractor
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_equal_length


class OldFlAnalogManager:

    @beartype
    def __init__(self, analog_files: list):
        validate_parameters_equal_length(__name__, analog_files)

        self.analog_files = analog_files

    @beartype
    def get_analog(self) -> FlAnalog:
        """"extract data from analog files"""

        all_analog_data = []
        number_of_datasets = len(self.analog_files)
        for i in range(number_of_datasets):
            all_analog_data.append(
                OldFlAnalogExtractor.extract_analog_for_single_dataset(
                    self.analog_files[i]
                )
            )
        merged_epochs = self.__merge_epochs(all_analog_data)
        description = self.__merge_row_description(all_analog_data)
        analog_data = self.__merge_analog_sensors(merged_epochs)

        timestamps = []
        return OldFlAnalogBuilder.build(analog_data, timestamps, description)

    @staticmethod
    def __merge_epochs(data_from_multiple_datasets):
        merged_epochs = data_from_multiple_datasets[0]
        for single_dataset_data in data_from_multiple_datasets[1:]:
            for row in single_dataset_data.keys():
                merged_epochs[row] = np.hstack((merged_epochs[row], single_dataset_data[row]))
        return merged_epochs

    @staticmethod
    def __merge_row_description(data_from_multiple_datasets):
        row_ids = data_from_multiple_datasets[0].keys()
        description = ''
        for id in row_ids:
            description += id + '   '
        return description

    @classmethod
    def __merge_analog_sensors(cls, merged_epochs):
        analog_sensors = [merged_epochs[analog_sensor] for analog_sensor in merged_epochs.keys() if
                          'timestamp' not in analog_sensor]
        merged_analog_sensors = np.array(analog_sensors, np.int32)
        transposed_analog_data = np.ndarray.transpose(merged_analog_sensors)
        return transposed_analog_data
