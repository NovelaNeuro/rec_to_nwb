from fl.datamigration.nwb.components.valid_times.valid_time_builder import ValidTimeBuilder


class ValidTimeManager:
    def __init__(self, sampling_rate):
        self.sampling_rate = sampling_rate
        self.mda_valid_time_builder = ValidTimeBuilder(sampling_rate)

    def build(self, timestamps):
        return self.mda_valid_time_builder.build(timestamps)
