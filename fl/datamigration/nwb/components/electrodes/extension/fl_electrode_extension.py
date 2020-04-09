class FlElectrodeExtension:

    def __init__(self, rel, hw_chan, ntrode_id, bad_channels):
        self.rel_x = rel['rel_x']
        self.rel_y = rel['rel_y']
        self.rel_z = rel['rel_z']
        self.hw_chan = hw_chan
        self.ntrode_id = ntrode_id
        self.bad_channels = bad_channels
