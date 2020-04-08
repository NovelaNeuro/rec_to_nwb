from fl.datamigration.nwb.components.mda.mda_valid_time_builder import MdaValidTimeBuilder


class MdaValidTimeManager:
    def __init__(self, sampling_rate):
        self.sampling_rate = sampling_rate
        self.mda_valid_time_builder = MdaValidTimeBuilder(sampling_rate)

    def build(self, timestamps):
        return self.mda_valid_time_builder.build(timestamps)
