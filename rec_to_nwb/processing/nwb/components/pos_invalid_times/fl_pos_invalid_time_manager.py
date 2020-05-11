from rec_to_nwb.processing.nwb.components.pos_invalid_times.fl_invalid_time_pos_timestamp_extractor import \
    FlInvalidTimePosTimestampExtractor
from rec_to_nwb.processing.nwb.components.pos_invalid_times.fl_pos_invalid_time_builder import FlPosInvalidTimeBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlPosInvalidTimeManager:

    @beartype
    def __init__(self, datasets: list):
        self.datasets = datasets

        self.period_multiplier = 1.5
        self.pos_timestamps_extractor = FlInvalidTimePosTimestampExtractor(datasets)

    def get_pos_invalid_times(self):
        timestamps = self.pos_timestamps_extractor.get_converted_timestamps()
        return self.__build_pos_invalid_times(timestamps, self.__calculate_pos_period(timestamps))

    def __build_pos_invalid_times(self, timestamps, period):
        gaps = []
        unfinished_gap = None
        for i, single_epoch_timestamps in enumerate(timestamps):
            gaps.extend(
                self.__build_gaps_from_single_epoch(
                    single_epoch_timestamps,
                    period,
                    unfinished_gap
                    )
            )
            if gaps and not i == len(timestamps)-1 and gaps[-1].stop_time == single_epoch_timestamps[-1]:
                unfinished_gap = gaps.pop()
        return gaps

    def __build_gaps_from_single_epoch(self, timestamps, period=None, unfinished_gap=None, last_timestamp=None):
        gap_start_time, gap_stop_time = timestamps[0], timestamps[0]
        gaps = []
        if unfinished_gap:
            was_last_timestamp_part_of_a_gap = True
            gap_start_time = unfinished_gap.start_time
            last_timestamp = gap_start_time
        else:
            was_last_timestamp_part_of_a_gap = False
            if not last_timestamp:
                last_timestamp = timestamps[0]
        for timestamp in timestamps:
            if not was_last_timestamp_part_of_a_gap:
                if last_timestamp + (period * self.period_multiplier) < timestamp:
                    gap_start_time = last_timestamp
                    was_last_timestamp_part_of_a_gap = True
            else:
                if last_timestamp + (period * self.period_multiplier) >= timestamp:
                    gap_stop_time = last_timestamp
                    was_last_timestamp_part_of_a_gap = False
                    gaps.append(FlPosInvalidTimeBuilder.build(gap_start_time, gap_stop_time))
                elif timestamp == timestamps[-1]:
                    gap_stop_time = timestamp
                    gaps.append(FlPosInvalidTimeBuilder.build(gap_start_time, gap_stop_time))
            last_timestamp = timestamp
        return gaps

    @staticmethod
    def __calculate_pos_period(timestamps):
        number_of_invalid_records_at_start_of_a_file = 0
        number_of_invalid_records_at_end_of_a_file = 0
        first_timestamp = timestamps[0][0]
        last_timestamp = timestamps[-1][-1]
        len_of_timestamps = sum([len(single_epoch_timestamps) for single_epoch_timestamps in timestamps])
        while not first_timestamp >= 0:
            number_of_invalid_records_at_start_of_a_file += 1
            first_timestamp = timestamps[0][number_of_invalid_records_at_start_of_a_file]
        while not last_timestamp >= 0:
            number_of_invalid_records_at_end_of_a_file += 1
            last_timestamp = timestamps[-1][(-1 - number_of_invalid_records_at_end_of_a_file)]
        return (last_timestamp - first_timestamp) / \
               (len_of_timestamps - number_of_invalid_records_at_end_of_a_file -
                number_of_invalid_records_at_start_of_a_file)