from rec_to_nwb.processing.nwb.components.mda_invalid_times.fl_mda_invalid_time_builder import FlMdaInvalidTimeBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlMdaInvalidTimeManager:

    @beartype
    def __init__(self, sampling_rate: float, period_multiplier: float):
        self.sampling_rate = sampling_rate
        self.period_multiplier = period_multiplier

        # self.period_multiplier = 1.5

    @beartype
    def get_mda_invalid_times(self, timestamps: list) -> list:
        invalid_times = self.__get_mda_invalid_times(timestamps)
        fl_mda_invalid_times = [FlMdaInvalidTimeBuilder.build(gap[0], gap[1]) for gap in invalid_times]
        return fl_mda_invalid_times

    def __get_mda_invalid_times(self, timestamps, period, eps=0.0001):
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
            first_timestamp = timestamps[number_of_invalid_records_at_start_of_a_file]
        while not last_timestamp >= 0:
            number_of_invalid_records_at_end_of_a_file += 1
            last_timestamp = timestamps[(-1 - number_of_invalid_records_at_end_of_a_file)]
        return (last_timestamp - first_timestamp) / \
               (len_of_timestamps - number_of_invalid_records_at_end_of_a_file -
                number_of_invalid_records_at_start_of_a_file)




    #
    # def get_mda_invalid_times(self, eps=0.0001):
    #     invalid_times = []
    #     gap_between_datasets = False
    #     last_dataset_last_timestamp = None
    #     for epoch in self.datasets:
    #         continuous_time_dict = self.fl_invalid_time_mda_extractor.get_continuous_time_dict(epoch)
    #         gaps_lower_bounds, gaps_upper_bounds = self.get_invalid_times_from_single_epoch(epoch)
    #         converted_upper_bounds = self.convert_timestamps_in_invalid_times_from_single_epoch(
    #             gaps_upper_bounds,
    #             continuous_time_dict
    #         )
    #         converted_lower_bounds = self.convert_timestamps_in_invalid_times_from_single_epoch(
    #             gaps_lower_bounds,
    #             continuous_time_dict
    #         )
    #         converted_upper_bounds = converted_upper_bounds - eps
    #         converted_lower_bounds = converted_lower_bounds + eps
    #         if last_dataset_last_timestamp and self.check_for_gap_between_datasets(
    #                 expected_time_between_timestamps=1E9 / self.sampling_rate,
    #                 timestamps=[
    #                     last_dataset_last_timestamp,
    #                     self.fl_invalid_time_mda_extractor.get_sample_count_from_single_epoch(epoch)
    #                 ]
    #         ):
    #             gap_between_datasets = True
    #         for i, lower_bound in enumerate(converted_lower_bounds):
    #             invalid_times.append(FlMdaInvalidTimeBuilder.build(
    #                 lower_bound,
    #                 converted_upper_bounds[i],
    #             )
    #             )
    #             if i == 0 and gap_between_datasets:
    #                 gap_between_datasets = self.__add_gap_between_epochs(gap_between_datasets, invalid_times, eps)
    #             last_dataset_last_timestamp = invalid_times[-1].stop_time
    #     return invalid_times
    #
    # def __add_gap_between_epochs(self, gap_between_datasets, invalid_times, eps):
    #     if invalid_times[-1].start_time == invalid_times[-2].stop_time - eps:
    #         first_gap_from_current_epoch = invalid_times.pop()
    #         last_gap_from_previous_dataset = invalid_times.pop()
    #         invalid_times.append(FlMdaInvalidTimeBuilder.build(
    #             first_gap_from_current_epoch.start_time,
    #             last_gap_from_previous_dataset.stop_time
    #         )
    #         )
    #         gap_between_datasets = False
    #     return gap_between_datasets
    #
    # def check_for_gap_between_datasets(self, expected_time_between_timestamps, timestamps):
    #     if timestamps[0] + expected_time_between_timestamps < timestamps[1]:
    #         return True
    #     return False
    #
    # def get_invalid_times_from_single_epoch(self, epoch):
    #     gaps_upper_bounds, gaps_lower_bounds = self.get_invalid_times_from_single_epoch_raw_timestamps(
    #         self.fl_invalid_time_mda_extractor.get_sample_count_from_single_epoch(epoch)
    #     )
    #     return gaps_lower_bounds, gaps_upper_bounds
    #
    # def get_invalid_times_from_single_epoch_raw_timestamps(self, sample_count):
    #     lower_bounds = (sample_count + 1)[:-1]
    #     upper_bounds = (sample_count - 1)[1:]
    #     mask = lower_bounds <= upper_bounds
    #     upper_bounds, lower_bounds = upper_bounds[mask] + 1, lower_bounds[mask] - 1
    #     filtered_lower_bounds = lower_bounds
    #     filtered_upper_bounds = upper_bounds
    #     for element in upper_bounds:
    #         filtered_lower_bounds = filtered_lower_bounds[filtered_lower_bounds != element]
    #     for element in lower_bounds:
    #         filtered_upper_bounds = filtered_upper_bounds[filtered_upper_bounds != element]
    #     return filtered_upper_bounds, filtered_lower_bounds
    #
    # def convert_timestamps_in_invalid_times_from_single_epoch(self, timestamps, continuous_time_dict):
    #     return TimestampConverter.convert_timestamps(continuous_time_dict, timestamps)
