from rec_to_nwb.processing.time.continuous_time_extractor import ContinuousTimeExtractor
from rec_to_nwb.processing.time.timestamp_converter import TimestampConverter

from mountainlab_pytools.mdaio import readmda

from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.dataset import Dataset


class FlInvalidTimeMdaTimestampExtractor:
    @beartype
    def get_sample_count_from_single_epoch(self, epoch: Dataset):
        return self.__read_mda_timestamps_from_single_epoch(self.__get_mda_timestamp_file(epoch))

    def __read_mda_timestamps_from_single_epoch(self, timestamp_file):
        return readmda(timestamp_file)

    @staticmethod
    @beartype
    def get_continuous_time_dict(epoch: Dataset):
        continuous_time_extractor = ContinuousTimeExtractor()
        continuous_time_file = epoch.get_continuous_time()
        return continuous_time_extractor.get_continuous_time_dict([continuous_time_file])[0]

    @staticmethod
    def __convert_timestamps(timestamps, continuous_time_dicts):
        return TimestampConverter.convert_timestamps(continuous_time_dicts, timestamps)

    def __get_mda_timestamp_file(self, epoch):
        return epoch.get_mda_timestamps()
