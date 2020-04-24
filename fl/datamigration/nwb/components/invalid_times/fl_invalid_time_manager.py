from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_builder import FlInvalidTimeBuilder
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

    def _validate_parameters(self):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.datasets))
        validation_registrator.validate()
