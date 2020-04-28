from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_mda_timestamp_extractor import \
    FlInvalidTimeMdaTimestampExtractor
from fl.datamigration.nwb.components.invalid_times.fl_mda_invalid_time_builder import FlMdaInvalidTimeBuilder
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class FlMdaInvalidTimeManager:
    def __init__(self, sampling_rate, datasets):
        self.sampling_rate = sampling_rate
        self.period_multiplier = 1.5
        self.datasets = datasets

        self.__validate_parameters()
        self.timestamps_extractor = FlInvalidTimeMdaTimestampExtractor(datasets)

    def build(self, timestamps, period):
        gaps = []
        unfinished_gap = None
        for i,single_epoch_timestamps in enumerate(timestamps):
            gaps.extend(self.__build_gaps_from_single_epoch(single_epoch_timestamps,
                                                            period,
                                                            unfinished_gap
                                                            ))
            if gaps:
                if not i == len(timestamps)-1:
                    if gaps[-1].stop_time == single_epoch_timestamps[-1]:
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
                    gaps.append(FlMdaInvalidTimeBuilder.build(gap_start_time, gap_stop_time))
                elif timestamp == timestamps[-1]:
                    gap_stop_time = timestamp
                    gaps.append(FlMdaInvalidTimeBuilder.build(gap_start_time, gap_stop_time))
            last_timestamp = timestamp
        return gaps

    def build_mda_invalid_times(self):
        return self.build(self.timestamps_extractor.get_converted_timestamps(),
                          1E9/self.sampling_rate)

    def __validate_parameters(self):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.sampling_rate))
        validation_registrator.register(NotNoneValidator(self.datasets))
        validation_registrator.validate()
