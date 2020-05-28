import numpy as np

from rec_to_nwb.processing.nwb.components.pos_valid_times.fl_pos_valid_time_builder import FlPosValidTimeBuilder
from rec_to_nwb.processing.nwb.components.pos_valid_times.fl_valid_time_pos_timestamp_extractor import \
    FlValidTimePosTimestampExtractor
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlPosValidTimeManager:

    @beartype
    def __init__(self, datasets: list):
        self.datasets = datasets

        self.period_multiplier = 1.5
        self.pos_timestamps_extractor = FlValidTimePosTimestampExtractor(datasets)

    def get_pos_valid_times(self):
        timestamps = self.get_pos_timestamps()
        return self.__build_pos_valid_times(timestamps, self.__calculate_pos_period(timestamps))

    def get_pos_timestamps(self):
        timestamps = self.pos_timestamps_extractor.get_converted_timestamps()
        return np.hstack(timestamps)

    def __build_pos_valid_times(self, timestamps, period):
        valid_times = self.__get_pos_valid_times(timestamps, period)
        fl_invalid_times = [FlPosValidTimeBuilder.build(gap[0], gap[1]) for gap in valid_times]
        return fl_invalid_times

    def __get_pos_valid_times(self, timestamps, period, eps=0.0001):
        min_valid_len = 3*eps
        timestamps = timestamps[~np.isnan(timestamps)]
        gaps = np.diff(timestamps) > period * self.period_multiplier
        gap_indexes = np.asarray(np.where(gaps))
        gap_start = np.insert(gap_indexes + 1, 0, 0)
        gap_end = np.append(gap_indexes, np.asarray(len(timestamps)-1))
        valid_indices = np.vstack([gap_start, gap_end]).transpose()
        valid_times = timestamps[valid_indices]
        valid_times[:, 0] = valid_times[:, 0] + eps
        valid_times[:, 1] = valid_times[:, 1] - eps
        valid_intervals = (valid_times[:, 1] - valid_times[:, 0]) > min_valid_len
        return valid_times[valid_intervals, :]

    @staticmethod
    def __calculate_pos_period(timestamps):
        number_of_invalid_records_at_start_of_a_file = 0
        number_of_invalid_records_at_end_of_a_file = 0
        first_timestamp = timestamps[0]
        last_timestamp = timestamps[-1]
        len_of_timestamps = len(timestamps)
        while not first_timestamp >= 0:
            number_of_invalid_records_at_start_of_a_file += 1
            first_timestamp = timestamps[number_of_invalid_records_at_start_of_a_file]
        while not last_timestamp >= 0:
            number_of_invalid_records_at_end_of_a_file += 1
            last_timestamp = timestamps[(-1 - number_of_invalid_records_at_end_of_a_file)]
        return (last_timestamp - first_timestamp) / \
               (len_of_timestamps - number_of_invalid_records_at_end_of_a_file -
                number_of_invalid_records_at_start_of_a_file)