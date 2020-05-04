from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor
from fl.datamigration.processing.timestamp_converter import TimestampConverter

from mountainlab_pytools.mdaio import readmda


class FlInvalidTimeMdaTimestampExtractor:
    def get_raw_timestamps_from_single_epoch(self, epoch):
        return self.read_mda_timestamps_from_single_epoch(self.__get_mda_timestamp_file(epoch))

    def read_mda_timestamps_from_single_epoch(self, timestamp_file):
        return readmda(timestamp_file)

    def get_mda_timestamp_file(self, epoch):
        return epoch.get_mda_timestamps()

    @staticmethod
    def get_continuous_time_dict(epoch):
        continuous_time_extractor = ContinuousTimeExtractor()
        continuous_time_file = epoch.get_continuous_time()
        return continuous_time_extractor.get_continuous_time_dict([continuous_time_file])[0]

    @staticmethod
    def __convert_timestamps(timestamps, continuous_time_dicts):
        return TimestampConverter.convert_timestamps(continuous_time_dicts, timestamps)

    def __get_mda_timestamp_file(self, epoch):
        return epoch.get_mda_timestamps()
