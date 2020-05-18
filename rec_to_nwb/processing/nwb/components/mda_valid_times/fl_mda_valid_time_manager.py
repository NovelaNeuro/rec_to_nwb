import numpy as np

from rec_to_nwb.processing.nwb.components.mda_valid_times.fl_valid_time_mda_timestamp_extractor import \
    FlValidTimeMdaTimestampExtractor
from rec_to_nwb.processing.nwb.components.mda_valid_times.fl_mda_valid_time_builder import FlMdaValidTimeBuilder
from rec_to_nwb.processing.time.timestamp_converter import TimestampConverter
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlMdaValidTimeManager:

    @beartype
    def __init__(self, sampling_rate: float, datasets: list):
        self.sampling_rate = sampling_rate
        self.datasets = datasets

        self.period_multiplier = 1.5
        self.period = 1E9 / sampling_rate
        self.fl_valid_time_mda_extractor = FlValidTimeMdaTimestampExtractor()

    # def __get_mda_valid_times_from_single_epoch(self, timestamps, period, eps=0.0001):
    #     min_valid_len = 3*eps
    #
    #     valid_times[:, 0] = valid_times[:, 0] + eps
    #     valid_times[:, 1] = valid_times[:, 1] - eps
    def get_mda_valid_times(self):
        timestamps = [self.fl_valid_time_mda_extractor.get_sample_count_from_single_epoch(epoch) for epoch in self.datasets]
        return self.__build_mda_valid_times(timestamps)

    def __build_mda_valid_times(self, timestamps):
        valid_times = self.__get_mda_valid_times(timestamps)
        fl_invalid_times = [FlMdaValidTimeBuilder.build(gap[0], gap[1]) for gap in valid_times]
        return fl_invalid_times

    def __get_mda_valid_times(self, timestamps, eps=0.0001):
        min_valid_len = 1
        all_valid_times = []
        last_dataset_last_timestamp = None
        for i, single_epoch_timestamps in enumerate(timestamps):
            single_epoch_timestamps = single_epoch_timestamps[~np.isnan(single_epoch_timestamps)]
            gaps = np.diff(single_epoch_timestamps) > 1
            gap_indexes = np.asarray(np.where(gaps))
            gap_start = np.insert(gap_indexes + 1, 0, 0)
            gap_end = np.append(gap_indexes, np.asarray(len(single_epoch_timestamps) - 1))
            valid_indices = np.vstack([gap_start, gap_end]).transpose()
            valid_times = single_epoch_timestamps[valid_indices]
            valid_intervals = (valid_times[:, 1] - valid_times[:, 0]) > min_valid_len
            continuous_time_dict = self.fl_valid_time_mda_extractor.get_continuous_time_dict(self.datasets[i])
            converted_intervals = np.ndarray(shape=np.shape(valid_times[valid_intervals, :]), dtype='float')
            converted_intervals[:, 0] = TimestampConverter.convert_timestamps(
                continuous_time_dict,
                valid_times[valid_intervals, 0]
            )
            converted_intervals[:, 1] = TimestampConverter.convert_timestamps(
                continuous_time_dict,
                valid_times[valid_intervals, 1]
            )
            last_epoch_last_timestamp = 0
            if last_dataset_last_timestamp:
                if not self.check_for_gap_between_datasets(
                        [single_epoch_timestamps[-1],
                        last_dataset_last_timestamp]
                ):
                    if all_valid_times[-1][-1, 1] == converted_intervals[0, 0]:
                        all_valid_times[-1][-1, 1] = converted_intervals[0, 1]
                    elif last_epoch_last_timestamp == converted_intervals[0, 0]:
                        all_valid_times[-1][-1, 1] = single_epoch_timestamps[-1]
                    elif single_epoch_timestamps[-1] == all_valid_times[-1][-1, 1]:
                        all_valid_times[-1][-1, 1] = last_epoch_last_timestamp
            last_dataset_last_timestamp = single_epoch_timestamps[-1]
            all_valid_times.append(
                converted_intervals
            )
        stacked_valid_times = np.hstack(all_valid_times)
        stacked_valid_times[:, 0] = stacked_valid_times[:, 0] + eps
        stacked_valid_times[:, 1] = stacked_valid_times[:, 1] - eps
        return stacked_valid_times

    def check_for_gap_between_datasets(self, timestamps):
        if timestamps[0] + (self.period * self.period_multiplier) < timestamps[1]:
            return True
        return False

    def get_valid_times_from_single_epoch(self, epoch):
        gaps_upper_bounds, gaps_lower_bounds = self.get_valid_times_from_single_epoch_raw_timestamps(
            self.fl_valid_time_mda_extractor.get_sample_count_from_single_epoch(epoch))
        return gaps_lower_bounds, gaps_upper_bounds

    def get_valid_times_from_single_epoch_raw_timestamps(self, sample_count):
        lower_bounds = (sample_count + 1)[:-1]
        upper_bounds = (sample_count - 1)[1:]
        mask = lower_bounds <= upper_bounds
        upper_bounds, lower_bounds = upper_bounds[mask] + 1, lower_bounds[mask] -1
        filtered_lower_bounds = lower_bounds
        filtered_upper_bounds = upper_bounds
        for element in upper_bounds:
            filtered_lower_bounds = filtered_lower_bounds[filtered_lower_bounds != element]
        for element in lower_bounds:
            filtered_upper_bounds = filtered_upper_bounds[filtered_upper_bounds != element]
        return filtered_upper_bounds, filtered_lower_bounds

    def convert_timestamps_in_valid_times_from_single_epoch(self, timestamps, continuous_time_dict):
        return TimestampConverter.convert_timestamps(continuous_time_dict, timestamps)
