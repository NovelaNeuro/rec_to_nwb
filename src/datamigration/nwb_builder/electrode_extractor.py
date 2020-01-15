class ElectrodeExtractor:
    def __init__(self, probes):
        self.probes = probes

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

        # ToDo Thats wrong of course. Iterate over two sets of data
        # for electrode in electrodes:
        #     for spike_trodes in Header('Header.xml').configuration.spike_configuration.spike_n_trodes:
        #         for spiken_channel in spike_trodes.spike_channels:
        #             electrode["hwChan"] = spiken_channel.hw_chan

        return electrodes

    def get_all_electrodes(self):
        electrodes = []
        for probe in self.probes:
            electrodes = electrodes + self.get_all_electrodes_from_probe(probe)
        return electrodes
