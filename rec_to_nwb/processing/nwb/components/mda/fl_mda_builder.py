from rec_to_nwb.processing.nwb.components.mda.fl_mda import FlMda


class FlMdaBuilder:

    def __init__(self, sampling_rate):
        self.sampling_rate = sampling_rate

    def build(self, electrode_table_region, data):
        return FlMda(self.sampling_rate, electrode_table_region, data)
