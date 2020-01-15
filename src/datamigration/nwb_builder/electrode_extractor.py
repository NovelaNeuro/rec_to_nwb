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
                electrode["electrode_group"] = shank["electrode_group_name"]
            electrodes = electrodes + electrodes_from_current_shank
        for electrode in electrodes:
            electrode["probe"] = probe_dict["id"]
        return electrodes

    def get_all_electrodes(self):
        electrodes = []
        for probe in self.probes:
            electrodes = electrodes + self.get_all_electrodes_from_probe(probe)
        return electrodes
