from rec_to_nwb.processing.nwb.components.pos_invalid_times.fl_invalid_time_pos_timestamp_extractor import \
    FlInvalidTimePosTimestampExtractor
from rec_to_nwb.processing.nwb.components.pos_invalid_times.fl_pos_invalid_time_builder import FlPosInvalidTimeBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype
import numpy as np

class FlPosInvalidTimeManager:

    @beartype
    def __init__(self, datasets: list):
        self.datasets = datasets

        self.period_multiplier = 1.5
        self.pos_timestamps_extractor = FlInvalidTimePosTimestampExtractor(datasets)

    def get_pos_timestamps(self):
        timestamps = self.pos_timestamps_extractor.get_converted_timestamps()
        return np.hstack(timestamps)


    def get_pos_invalid_times(self):
        timestamps = self.get_pos_timestamps()
        return self.__build_pos_invalid_times(timestamps, self.__calculate_pos_period(timestamps))

    def __build_pos_invalid_times(self, timestamps, period):
        invalid_times = self.__get_pos_invalid_times(timestamps, period)
        fl_invalid_times = []
        for gap in invalid_times:
            fl_invalid_times.append(FlPosInvalidTimeBuilder.build(gap[0], gap[1]))
        return fl_invalid_times

    def __get_pos_valid_times(self, timestamps, period, eps=0.0001):
        min_valid_len = 3*eps
        timestamps = timestamps[~np.isnan(timestamps)]
        gaps = np.diff(timestamps) > period * self.period_multiplier
        gapind = np.asarray(np.where(gaps))
        gap_start = np.insert(gapind + 1, 0, 0)
        gap_end = np.append(gapind, np.asarray(len(timestamps)-1))
        valid_indices = np.vstack([gap_start, gap_end]).transpose()
        valid_times = timestamps[valid_indices]
        valid_times[:, 0] = valid_times[:, 0] + eps
        valid_times[:, 1] = valid_times[:, 1] - eps
        valid_intervals = (valid_times[:, 1] - valid_times[:, 0]) > min_valid_len
        return valid_times[valid_intervals, :]

    def __get_pos_invalid_times(self, timestamps, period, eps=0.0001):
        min_valid_len = 3 * eps
        valid_times = self.__get_pos_valid_times(timestamps, period, eps)
        start_times = np.append(np.asarray(timestamps[0] + eps), (valid_times[:, 1] + 2 * eps))
        stop_times = np.append(valid_times[:, 0] - 2 * eps, np.asarray(timestamps[-1] - eps))
        invalid_times = (np.vstack([start_times, stop_times])).transpose()
        valid_intervals = (invalid_times[:, 1] - invalid_times[:, 0]) > min_valid_len

        return invalid_times[valid_intervals, :]


    @staticmethod
    def __calculate_pos_period(timestamps):
        number_of_invalid_records_at_start_of_a_file = 0
        number_of_invalid_records_at_end_of_a_file = 0
        first_timestamp = timestamps[0]
        last_timestamp = timestamps[-1]
        len_of_timestamps = len(timestamps)
        while not first_timestamp >= 0:
            number_of_invalid_records_at_start_of_a_file += 1
            first_timestamp = timestamps[0][number_of_invalid_records_at_start_of_a_file]
        while not last_timestamp >= 0:
            number_of_invalid_records_at_end_of_a_file += 1
            last_timestamp = timestamps[-1][(-1 - number_of_invalid_records_at_end_of_a_file)]
        return (last_timestamp - first_timestamp) / \
               (len_of_timestamps - number_of_invalid_records_at_end_of_a_file -
                number_of_invalid_records_at_start_of_a_file)