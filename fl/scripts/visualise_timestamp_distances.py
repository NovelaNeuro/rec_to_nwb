from mountainlab_pytools.mdaio import readmda

from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor
from fl.datamigration.processing.timestamp_converter import TimestampConverter


def read_mda_timestamps(file):
    return readmda(file)


if __name__ == "__main__":
    timestamps_files = []
    continuous_time_files = []

    timestamps = [read_mda_timestamps(timestamps_file) for timestamps_file in timestamps_files]
    continuous_time_extractor = ContinuousTimeExtractor()
    continuous_time_dicts = continuous_time_extractor.get_continuous_time_dict(continuous_time_files)

    distances = []
    for i, continuous_time_dict in enumerate(continuous_time_dicts):
        converted_timestamps = TimestampConverter.convert_timestamps(continuous_time_dict, timestamps[i])
        for j in range(1, len(converted_timestamps)):
            distances.append(converted_timestamps[j] - converted_timestamps[j - 1])


