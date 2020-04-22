import pandas as pd

from mountainlab_pytools.mdaio import readmda
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from fl.datamigration.nwb.components.invalid_times.invalid_time_builder import InvalidTimeBuilder
from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor
from fl.datamigration.processing.timestamp_converter import TimestampConverter
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class InvalidTimeManager:
    def __init__(self, sampling_rate, datasets):
        self.sampling_rate = sampling_rate
        self.datasets = datasets

        self.__validate_parameters()

        self.invalid_time_builder = InvalidTimeBuilder(sampling_rate)
        self.mda_timestamp_files = self.__get_mda_timestamp_files()
        self.pos_timestamp_files = self.__get_pos_files()

    def build(self, timestamps, data_type):
        gaps = []
        unfinished_gap = None
        for single_epoch_timestamps in timestamps:
            gaps.extend(self.invalid_time_builder.build(single_epoch_timestamps, data_type, unfinished_gap))
            if gaps:
                if gaps[-1].stop_time == single_epoch_timestamps[-1]:
                    unfinished_gap = gaps.pop()
        return gaps

    def build_mda_invalid_times(self):
        continuous_time_dicts = self.__get_continuous_time_dicts()
        mda_timestamps = self.__read_mda_timestamps(self.__get_mda_timestamp_files())
        return self.build(self.__convert_timestamps(mda_timestamps, continuous_time_dicts), 'mda')

    def build_pos_invalid_times(self):
        continuous_time_dicts = self.__get_continuous_time_dicts()
        pos_timestamps = self.__read_pos_timestamps(self.__get_pos_files())
        return self.build(self.__convert_timestamps(pos_timestamps, continuous_time_dicts), 'pos')

    def __convert_timestamps(self, timestamps, continuous_time_dicts):
        return [TimestampConverter.convert_timestamps(continuous_time_dicts[i], timestamp)
                for i, timestamp in enumerate(timestamps)]

    def __get_continuous_time_dicts(self):
        continuous_time_extractor = ContinuousTimeExtractor()
        continuous_time_files = [dataset.get_continuous_time() for dataset in self.datasets]
        return continuous_time_extractor.get_continuous_time_dict(continuous_time_files)

    def __get_mda_timestamp_files(self):
        return [dataset.get_mda_timestamps() for dataset in self.datasets]

    def __get_pos_files(self):
        all_files = []
        for dataset in self.datasets:
            single_dataset_files = dataset.get_all_data_from_dataset('pos')
            for file in single_dataset_files:
                if file.endswith('pos_online.dat'):
                    all_files.append(dataset.get_data_path_from_dataset('pos') + file)
        return all_files

    def __read_mda_timestamps(self, timestamp_files):
        return [readmda(timestamp_file) for timestamp_file in timestamp_files]

    def __read_pos_timestamps(self, timestamp_files):
        return [self.__read_single_pos_timestamps(timestamp_file) for timestamp_file in timestamp_files]

    def __read_single_pos_timestamps(self, timestamp_file):
        pos_online = readTrodesExtractedDataFile(timestamp_file)
        position = pd.DataFrame(pos_online['data'])
        return position.time.to_numpy(dtype='int64')

    def __validate_parameters(self):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.sampling_rate))
        validation_registrator.register(NotNoneValidator(self.datasets))
        validation_registrator.validate()
