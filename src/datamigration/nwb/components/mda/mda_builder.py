from src.datamigration.nwb.components.mda.lf_mda import LfMda


class MdaBuilder:

    def __init__(self, sampling_rate):
        self.sampling_rate = sampling_rate

    def build(self, electrode_table_region, data):
        return LfMda(self.sampling_rate, electrode_table_region, data)
