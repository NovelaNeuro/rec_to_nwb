class LfMda:

    def __init__(self, sampling_rate, electrode_table_region, mda_data):
        """internal representation of mda data"""

        self.sampling_rate = sampling_rate
        self.electrode_table_region = electrode_table_region
        self.mda_data = mda_data
