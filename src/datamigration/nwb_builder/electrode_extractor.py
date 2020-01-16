class ElectrodeExtractor:
    def __init__(self, probes, header):
        self.probes = probes
        self.header = header

    def get_all_electrodes_from_probe(self, probe_dict):
        electrodes = []
        shanks = probe_dict["shanks"]
        for shank in shanks:
            electrodes_from_current_shank = shank["electrodes"]
            for electrode in electrodes_from_current_shank:
                electrode["shank_id"] = shank["shank_id"]
                electrode["electrode_group"] = shank["electrode_group_id"]
            electrodes = electrodes + electrodes_from_current_shank

        for electrode in electrodes:
            electrode["probe_id"] = probe_dict["id"]

        #obtain list of spike channels in header(header injection needs to be set properly)
        spike_channels_list = []
        for spike_trode in self.header.configuration.spike_configuration.spike_n_trodes:
            for spike_channel in spike_trode.spike_channels:
                spike_channels_list.append(spike_channel)

        #zip 2 iterables into single touple iteration
        for spike_channel, electrode in zip(spike_channels_list, electrodes):
            electrode["hwChan"] = spike_channel.hw_chan

        return electrodes

    def get_all_electrodes(self):
        electrodes = []
        for probe in self.probes:
            electrodes = electrodes + self.get_all_electrodes_from_probe(probe)
        return electrodes
