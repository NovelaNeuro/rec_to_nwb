from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_builder import FlInvalidTimeBuilder
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_pos_timestamp_extractor import \
    FlInvalidTimePosTimestampExtractor
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class FlPosInvalidTimeManager:
    def __init__(self, datasets):
        self.period_multiplier = 1.5
        self.datasets = datasets

        self.pos_timestamps_extractor = FlInvalidTimePosTimestampExtractor(datasets)
        self._validate_parameters()

    def build(self, timestamps, data_type, period):
        gaps = []
        unfinished_gap = None
        for i,single_epoch_timestamps in enumerate(timestamps):
            gaps.extend(self.build_gaps_from_single_epoch(single_epoch_timestamps,
                                                          period,
                                                          unfinished_gap
                                                          ))
            if gaps:
                if not i == len(timestamps)-1:
                    if gaps[-1].stop_time == single_epoch_timestamps[-1]:
                        unfinished_gap = gaps.pop()
        return gaps

    def build_gaps_from_single_epoch(self, timestamps, period=None, unfinished_gap=None, last_timestamp=None):
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
                    gaps.append(FlInvalidTimeBuilder.build(gap_start_time, gap_stop_time))
                elif timestamp == timestamps[-1]:
                    gap_stop_time = timestamp
                    gaps.append(FlInvalidTimeBuilder.build(gap_start_time, gap_stop_time))
            last_timestamp = timestamp
        return gaps

    def _validate_parameters(self):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.datasets))
        validation_registrator.validate()

    def build_pos_invalid_times(self):
        timestamps = self.pos_timestamps_extractor.get_converted_timestamps()
        return self.build(timestamps, 'pos', self.__calculate_pos_period(timestamps))

    def __calculate_pos_period(self, timestamps):
        number_of_invalid_records_at_start_of_a_file = 0
        number_of_invalid_records_at_end_of_a_file = 0
        first_timestamp = timestamps[0][0]
        last_timestamp = timestamps[-1][-1]
        len_of_timestamps = 0
        for single_epoch_timestamps in timestamps:
            len_of_timestamps += len(single_epoch_timestamps)
        while not first_timestamp >= 0:
            number_of_invalid_records_at_start_of_a_file += 1
            first_timestamp = timestamps[0][number_of_invalid_records_at_start_of_a_file]
        while not last_timestamp >= 0:
            number_of_invalid_records_at_end_of_a_file += 1
            last_timestamp = timestamps[-1][(-1 - number_of_invalid_records_at_end_of_a_file)]
        return (last_timestamp - first_timestamp) / \
               (len_of_timestamps - number_of_invalid_records_at_end_of_a_file -
                number_of_invalid_records_at_start_of_a_file)