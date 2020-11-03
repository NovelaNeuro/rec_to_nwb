from rec_to_nwb.processing.nwb.components.mda.fl_mda import FlMda


class FlMdaBuilder:

    def __init__(self, sampling_rate, conversion):
        self.sampling_rate = sampling_rate
        self.conversion = conversion

    def build(self, electrode_table_region, data):
        return FlMda(self.sampling_rate, self.conversion, electrode_table_region, data)
