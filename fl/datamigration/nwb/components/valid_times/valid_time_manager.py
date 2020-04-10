from fl.datamigration.nwb.components.valid_times.valid_time_builder import ValidTimeBuilder
from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor


class ValidTimeManager:
    def __init__(self, sampling_rate, datasets):
        self.sampling_rate = sampling_rate
        self.mda_valid_time_builder = ValidTimeBuilder(sampling_rate)
        self.datasets = datasets
        self.mda_timestamps = self.__get_mda_timestamps()
        self.mda_timestamps = self.__get_pos_timestamps()

    def build(self):
        return self.mda_valid_time_builder.build(self.timestamps)

    def __get_continuous_time_dicts(self):
        continuous_time_extractor = ContinuousTimeExtractor()
        continuous_time_files = [dataset.get_continuous_time() for dataset in self.datasets]
        return continuous_time_extractor.get_continuous_time_dict(continuous_time_files)

    def __get_mda_timestamps(self):
        return [dataset.get_mda_timestamps() for dataset in self.datasets]

    def __get_pos_timestamps(self):
        return []
