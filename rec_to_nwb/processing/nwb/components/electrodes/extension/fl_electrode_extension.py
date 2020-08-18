class FlElectrodeExtension:

    def __init__(self, rel_x, rel_y, rel_z, hw_chan, ntrode_id, channel_id, bad_channels, probe_shank, probe_electrode,
                 ref_elect_id):
        self.rel_x = [float(x) for x in rel_x]
        self.rel_y = [float(y) for y in rel_y]
        self.rel_z = [float(z) for z in rel_z]
        self.hw_chan = hw_chan
        self.ntrode_id = [int(n_id) for n_id in ntrode_id]
        self.channel_id = [int(c_id) for c_id in channel_id]
        self.bad_channels = [bool(bad_channel) for bad_channel in bad_channels]
        self.probe_shank = probe_shank
        self.probe_electrode = probe_electrode
        self.ref_elect_id = [int(ref_id) for ref_id in ref_elect_id]
