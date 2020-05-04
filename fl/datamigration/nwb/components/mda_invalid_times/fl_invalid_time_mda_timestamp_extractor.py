from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor
from fl.datamigration.processing.timestamp_converter import TimestampConverter
from fl.datamigration.tools.beartype.beartype import beartype

from mountainlab_pytools.mdaio import readmda


class FlInvalidTimeMdaTimestampExtractor:

    @beartype
    def __init__(self, datasets: list):
        self.datasets = datasets

    def get_converted_timestamps(self):
        return self.__convert_timestamps(self.__read_mda_timestamps(), self.__get_continuous_time_dicts())

    @staticmethod
    def __convert_timestamps(timestamps, continuous_time_dicts):
        return [TimestampConverter.convert_timestamps(continuous_time_dicts[i], timestamp)
                for i, timestamp in enumerate(timestamps)]

    def __read_mda_timestamps(self):
        return [readmda(timestamp_file) for timestamp_file in self.__get_mda_timestamp_files()]

    def __get_mda_timestamp_files(self):
        return [dataset.get_mda_timestamps() for dataset in self.datasets]

    def __get_continuous_time_dicts(self):
        continuous_time_extractor = ContinuousTimeExtractor()
        continuous_time_files = [dataset.get_continuous_time() for dataset in self.datasets]
        return continuous_time_extractor.get_continuous_time_dict(continuous_time_files)




