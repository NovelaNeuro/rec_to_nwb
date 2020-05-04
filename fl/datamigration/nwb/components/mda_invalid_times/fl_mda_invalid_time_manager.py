from fl.datamigration.nwb.components.mda_invalid_times.fl_invalid_time_mda_timestamp_extractor import \
    FlInvalidTimeMdaTimestampExtractor
from fl.datamigration.nwb.components.mda_invalid_times.fl_mda_invalid_time_builder import FlMdaInvalidTimeBuilder
from fl.datamigration.processing.timestamp_converter import TimestampConverter
from fl.datamigration.tools.beartype.beartype import beartype


class FlMdaInvalidTimeManager:

    @beartype
    def __init__(self, sampling_rate: float, datasets: list):
        self.sampling_rate = sampling_rate
        self.datasets = datasets

        self.period_multiplier = 1.5
        self.invalid_time_extractor = FlInvalidTimeMdaTimestampExtractor()

    def get_mda_invalid_times(self):
        invalid_times = []
        for epoch in self.datasets:
            continuous_time_dict = self.invalid_time_extractor.get_continuous_time_dict(epoch)
            gaps_lower_bounds, gaps_upper_bounds = self.get_invalid_times_from_single_epoch(epoch)
            converted_upper_bounds = self.convert_timestamps_in_invalid_times_from_single_epoch(
                gaps_upper_bounds,
                continuous_time_dict
            )
            converted_lower_bounds = self.convert_timestamps_in_invalid_times_from_single_epoch(
                gaps_lower_bounds,
                continuous_time_dict
            )
            for i in range(len(converted_lower_bounds)):
                invalid_times.append(FlMdaInvalidTimeBuilder.build(
                    converted_lower_bounds[i],
                    converted_upper_bounds[i]
                )
                )
        return invalid_times

    def get_invalid_times_from_single_epoch(self, epoch):
        gaps_upper_bounds, gaps_lower_bounds = self.get_invalid_times_from_single_epoch_raw_timestamps(
            self.invalid_time_extractor.get_raw_timestamps_from_single_epoch(epoch))
        return gaps_lower_bounds, gaps_upper_bounds

    def get_invalid_times_from_single_epoch_raw_timestamps(self, raw_timestamps):
        lowerBounds = (raw_timestamps + 1)[:-1]
        upperBounds = (raw_timestamps - 1)[1:]
        mask = lowerBounds <= upperBounds
        upperBounds, lowerBounds = upperBounds[mask] + 1, lowerBounds[mask] -1
        filtered_lowerBounds = lowerBounds
        filtered_upperBounds = upperBounds
        for element in upperBounds:
            filtered_lowerBounds = filtered_lowerBounds[filtered_lowerBounds != element]
        for element in lowerBounds:
            filtered_upperBounds = filtered_upperBounds[filtered_upperBounds != element]
        return filtered_upperBounds, filtered_lowerBounds

    def convert_timestamps_in_invalid_times_from_single_epoch(self, timestamps, continuous_time_dict):
        return TimestampConverter.convert_timestamps(continuous_time_dict, timestamps)
