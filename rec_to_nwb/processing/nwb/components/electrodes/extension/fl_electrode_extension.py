class FlElectrodeExtension:

    def __init__(self, rel_x, rel_y, rel_z, hw_chan, ntrode_id, channel_id, bad_channels, probe_shank, probe_electrode,
                 ref_elect_id):
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.rel_z = rel_z
        self.hw_chan = hw_chan
        self.ntrode_id = ntrode_id
        self.channel_id = channel_id
        self.bad_channels = bad_channels
        self.probe_shank = probe_shank
        self.probe_electrode = probe_electrode
        self.ref_elect_id = ref_elect_id
