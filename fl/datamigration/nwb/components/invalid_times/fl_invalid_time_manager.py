
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_builder import FlInvalidTimeBuilder
from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor
from fl.datamigration.processing.timestamp_converter import TimestampConverter
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class FlInvalidTimeManager:
    def __init__(self, datasets):
        self.datasets = datasets

        self._validate_parameters()

        self.fl_invalid_time_builder = FlInvalidTimeBuilder()

    def build(self, timestamps, data_type, period):
        gaps = []
        unfinished_gap = None
        for single_epoch_timestamps in timestamps:
            gaps.extend(self.fl_invalid_time_builder.build(single_epoch_timestamps,
                                                           data_type,
                                                           period,
                                                           unfinished_gap
                                                           ))
            if gaps:
                if gaps[-1].stop_time == single_epoch_timestamps[-1]:
                    unfinished_gap = gaps.pop()
        return gaps

    def _convert_timestamps(self, timestamps, continuous_time_dicts):
        return [TimestampConverter.convert_timestamps(continuous_time_dicts[i], timestamp)
                for i, timestamp in enumerate(timestamps)]

    def _get_continuous_time_dicts(self):
        continuous_time_extractor = ContinuousTimeExtractor()
        continuous_time_files = [dataset.get_continuous_time() for dataset in self.datasets]
        return continuous_time_extractor.get_continuous_time_dict(continuous_time_files)

    def _validate_parameters(self):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.datasets))
        validation_registrator.validate()
