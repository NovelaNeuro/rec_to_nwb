import numpy as np

from rec_to_nwb.processing.nwb.components.analog.fl_analog import FlAnalog
from rec_to_nwb.processing.nwb.components.analog.fl_analog_builder import FlAnalogBuilder
from rec_to_nwb.processing.nwb.components.analog.fl_analog_extractor import FlAnalogExtractor
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_equal_length


class FlAnalogManager:

    @beartype
    def __init__(self, analog_files: list,
                       continuous_time_files: list,
                       convert_timestamps: bool = True,
                       return_timestamps: bool = True,
                       ):
        validate_parameters_equal_length(__name__, analog_files, continuous_time_files)

        self.analog_files = analog_files
        self.continuous_time_files = continuous_time_files
        self.convert_timestamps = convert_timestamps
        self.return_timestamps = return_timestamps

    @beartype
    def get_analog(self) -> FlAnalog:
        """"extract data from analog files"""

        all_analog_data = []
        number_of_datasets = len(self.analog_files)
        for i in range(number_of_datasets):
            all_analog_data.append(
                FlAnalogExtractor.extract_analog_for_single_dataset(
                    self.analog_files[i],
                    self.continuous_time_files[i],
                    convert_timestamps=self.convert_timestamps
                )
            )
        merged_epochs = self.__merge_epochs(all_analog_data)
        description = self.__merge_row_description(all_analog_data)
        analog_data = self.__merge_analog_sensors(merged_epochs)

        if self.return_timestamps:
            timestamps = self.__get_timestamps(merged_epochs)
        else:
            timestamps = []
        return FlAnalogBuilder.build(analog_data, timestamps, description)

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

    @classmethod
    def __get_timestamps(cls, merged_epochs):
        for analog_sensor in merged_epochs.keys():
            if 'timestamps' in analog_sensor:
                return merged_epochs[analog_sensor]
