from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_manager import FlInvalidTimeManager
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_mda_timestamp_extractor import \
    FlInvalidTimeMdaTimestampExtractor
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class FlMdaInvalidTimeManager(FlInvalidTimeManager):
    def __init__(self, sampling_rate, datasets):
        FlInvalidTimeManager.__init__(self, datasets)
        self.sampling_rate = sampling_rate
        self.timestamps_extractor = FlInvalidTimeMdaTimestampExtractor(datasets)

    def build_mda_invalid_times(self):
        return self.build(self.timestamps_extractor.get_converted_timestamps(),
                          'mda',
                          1E9/self.sampling_rate)

    def __validate_parameters(self):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.sampling_rate))
        validation_registrator.register(NotNoneValidator(self.datasets))
        validation_registrator.validate()
