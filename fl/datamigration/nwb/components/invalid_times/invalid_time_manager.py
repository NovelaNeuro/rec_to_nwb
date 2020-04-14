from mountainlab_pytools.mdaio import readmda

from fl.datamigration.nwb.components.invalid_times.invalid_time_builder import InvalidTimeBuilder
from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor
from fl.datamigration.processing.timestamp_converter import TimestampConverter


class InvalidTimeManager:
    def __init__(self, sampling_rate, datasets):
        self.sampling_rate = sampling_rate
        self.valid_time_builder = InvalidTimeBuilder(sampling_rate)
        self.datasets = datasets
        self.mda_timestamp_files = self.__get_mda_timestamp_files()
        self.mda_timestamps = self.__get_pos_timestamps()

    def build(self, timestamps):
        return self.valid_time_builder.build(timestamps[0]) #naprawic

    def build_mda_valid_times(self):
        continuous_time_dicts = self.__get_continuous_time_dicts()
        mda_timestamps = self.__read_mda_timestamps(self.__get_mda_timestamp_files())
        return self.build(self.__convert_timestamps(mda_timestamps, continuous_time_dicts))

    def __convert_timestamps(self, timestamps, continuous_time_dicts):
        all_timestamps = []
        for i, timestamp in enumerate(timestamps):
            all_timestamps.append(TimestampConverter.convert_timestamps(continuous_time_dicts[i], timestamp))
        return all_timestamps

    def __get_continuous_time_dicts(self):
        continuous_time_extractor = ContinuousTimeExtractor()
        continuous_time_files = [dataset.get_continuous_time() for dataset in self.datasets]
        return continuous_time_extractor.get_continuous_time_dict(continuous_time_files)

    def __get_mda_timestamp_files(self):
        return [dataset.get_mda_timestamps() for dataset in self.datasets]

    def __read_mda_timestamps(self, timestamp_files):
        return [readmda(timestamp_file) for timestamp_file in timestamp_files]

    def __get_pos_timestamps(self):
        return []
