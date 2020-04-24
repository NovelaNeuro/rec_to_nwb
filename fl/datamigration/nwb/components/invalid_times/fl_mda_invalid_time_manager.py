from mountainlab_pytools.mdaio import readmda

from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_manager import FlInvalidTimeManager
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class FlMdaInvalidTimeManager(FlInvalidTimeManager):
    def __init__(self, sampling_rate, datasets):
        FlInvalidTimeManager.__init__(self,datasets)
        self.sampling_rate = sampling_rate

    def build_mda_invalid_times(self):
        continuous_time_dicts = self._get_continuous_time_dicts()
        mda_timestamps = self.__read_mda_timestamps()
        return self.build(self._convert_timestamps(mda_timestamps, continuous_time_dicts),
                          'mda',
                          1E9/self.sampling_rate)

    def __get_mda_timestamp_files(self):
        return [dataset.get_mda_timestamps() for dataset in self.datasets]

    def __get_continuos_time_files(self):
        return [dataset.get_continuous_time() for dataset in self.datasets]

    def __read_mda_timestamps(self):
        return [readmda(timestamp_file) for timestamp_file in self.__get_mda_timestamp_files()]

    def __validate_parameters(self):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.sampling_rate))
        validation_registrator.register(NotNoneValidator(self.datasets))
        validation_registrator.validate()
