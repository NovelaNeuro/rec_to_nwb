import numpy as np

from rec_to_nwb.processing.nwb.components.mda_valid_times.fl_mda_valid_time_builder import FlMdaValidTimeBuilder
from rec_to_nwb.processing.nwb.components.mda_valid_times.fl_valid_time_mda_timestamp_extractor import \
    FlValidTimeMdaTimestampExtractor
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

    def get_mda_valid_times(self):
        timestamps = [self.fl_valid_time_mda_extractor.get_sample_count_from_single_epoch(epoch) for epoch in self.datasets]
        return self.__build_mda_valid_times(timestamps)

    def __build_mda_valid_times(self, timestamps):
        valid_times = self.__get_mda_valid_times(timestamps)
        return [FlMdaValidTimeBuilder.build(gap[0], gap[1]) for gap in valid_times]

    def __get_mda_valid_times(self, timestamps, eps=0.0001):
        min_valid_len = 1
        all_valid_times = []
        last_dataset_last_timestamp = None

        for counter, single_epoch_timestamps in enumerate(timestamps):
            single_epoch_timestamps = single_epoch_timestamps[~np.isnan(single_epoch_timestamps)]
            gap_end, gap_start = self.__get_gaps(single_epoch_timestamps)
            valid_times = self.__get_valid_times(gap_end, gap_start, single_epoch_timestamps)
            valid_intervals = self.__get_valid_intervals(min_valid_len, valid_times)
            converted_intervals = self.__get_converted_intervals(counter, valid_intervals, valid_times)
            self.__add_converted_timestamp_to_all_valid_times(
                all_valid_times,
                converted_intervals,
                last_dataset_last_timestamp,
                single_epoch_timestamps
            )
        return self.__get_stacked_valid_times(all_valid_times, eps)

    def __get_gaps(self, single_epoch_timestamps):
        gaps = np.diff(single_epoch_timestamps) > 1
        gap_indexes = np.asarray(np.where(gaps))
        gap_start = np.insert(gap_indexes + 1, 0, 0)
        gap_end = np.append(gap_indexes, np.asarray(len(single_epoch_timestamps) - 1))
        return gap_end, gap_start

    def __get_valid_times(self, gap_end, gap_start, single_epoch_timestamps):
        valid_indices = np.vstack([gap_start, gap_end]).transpose()
        return single_epoch_timestamps[valid_indices]

    def __get_valid_intervals(self, min_valid_len, valid_times):
        return (valid_times[:, 1] - valid_times[:, 0]) > min_valid_len


    def __get_converted_intervals(self, i, valid_intervals, valid_times):
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
        return converted_intervals

    def __add_converted_timestamp_to_all_valid_times(self, all_valid_times, converted_intervals,
                                                     last_dataset_last_timestamp, single_epoch_timestamps):
        last_epoch_last_timestamp = 0
        if last_dataset_last_timestamp:
            if not self.__check_for_gap_between_datasets(
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

    def __check_for_gap_between_datasets(self, timestamps):
        if timestamps[0] + (self.period * self.period_multiplier) < timestamps[1]:
            return True
        return False

    @staticmethod
    def __get_stacked_valid_times(all_valid_times, eps):
        stacked_valid_times = np.hstack(all_valid_times)
        stacked_valid_times[:, 0] = stacked_valid_times[:, 0] + eps
        stacked_valid_times[:, 1] = stacked_valid_times[:, 1] - eps
        return stacked_valid_times
