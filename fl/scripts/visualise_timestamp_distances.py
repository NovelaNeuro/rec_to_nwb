from mountainlab_pytools.mdaio import readmda

from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor
from fl.datamigration.processing.timestamp_converter import TimestampConverter

from matplotlib import pyplot


def read_mda_timestamps(file):
    return readmda(file)


if __name__ == "__main__":
    timestamps_files = ['C:/Users/wbodo/Desktop/resy/test/beans/preprocessing/20190718/20190718_beans_01_s1.mda/20190718_beans_01_s1.timestamps.mda']
    continuous_time_files = ['C:/Users/wbodo/Desktop/resy/test/beans/preprocessing/20190718/20190718_beans_01_s1.time/20190718_beans_01_s1.continuoustime.dat']

    timestamps = [read_mda_timestamps(timestamps_file) for timestamps_file in timestamps_files]
    continuous_time_extractor = ContinuousTimeExtractor()
    continuous_time_dicts = continuous_time_extractor.get_continuous_time_dict(continuous_time_files)

    distances = []
    max_distance = 0
    for i, continuous_time_dict in enumerate(continuous_time_dicts):
        converted_timestamps = TimestampConverter.convert_timestamps(continuous_time_dict, timestamps[i])
        for j in range(1, len(converted_timestamps) -1):
            if converted_timestamps[j] > 0 and converted_timestamps[j - 1] > 0:
                new_dist = (converted_timestamps[j] - converted_timestamps[j - 1])
                if new_dist > max_distance:
                    max_distance = new_dist

                distances.append(new_dist)

    pyplot.hist(distances, bins=4000, range=(0, max_distance))
    pyplot.show()
