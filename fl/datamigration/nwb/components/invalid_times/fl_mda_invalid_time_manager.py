from mountainlab_pytools.mdaio import readmda

from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_builder import InvalidTimeBuilder
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_manager import FlInvalidTimeManager
from fl.datamigration.nwb.components.mda.mda_timestamp_manager import MdaTimestampDataManager
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class FlMdaInvalidTimeManager(FlInvalidTimeManager):
    def __init__(self, sampling_rate, datasets):
        self.datasets = datasets

        self._validate_parameters()

        self.invalid_time_builder = InvalidTimeBuilder()
        self.sampling_rate = sampling_rate

    def get_fl_mda_invalid_times(self):



        fl_mda_invalid_times = []

        return fl_mda_invalid_times

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
        mda_timestamp_files = self.__get_mda_timestamp_files()
        continuos_time_files = self.__get_continuos_time_files()
        mda_timestamp_manager = MdaTimestampDataManager([mda_timestamp_files], continuos_time_files)
        return [mda_timestamp_manager.retrieve_real_timestamps(i) for i, dataset in enumerate(self.datasets)]

    def __validate_parameters(self):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.sampling_rate))
        validation_registrator.register(NotNoneValidator(self.datasets))
        validation_registrator.validate()
