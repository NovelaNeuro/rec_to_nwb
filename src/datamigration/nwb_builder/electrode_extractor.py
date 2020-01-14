import yaml


class ElectrodeExtractor:
    def __init__(self, probes):
        self.probes = probes

    def get_all_electrodes_from_probe(self, probe_path):
        electrodes = []
        with open(probe_path, 'r') as stream:
            probe_dict = yaml.safe_load(stream)
            shanks = probe_dict["shanks"]
            for shank in shanks:
                electrodes_from_current_shank = shank["electrodes"]
                for electrode in electrodes_from_current_shank:
                    electrode["shank"] = shank["id"]
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


if __name__ == "__main__":
    prbs = []
    prbs.append("C:/Users/wbodo/Documents/GitHub/LorenFranksDataMigration/src/test/datamigration/res/probe1.yml")
    prbs.append("C:/Users/wbodo/Documents/GitHub/LorenFranksDataMigration/src/test/datamigration/res/probe2.yml")
    prbs.append("C:/Users/wbodo/Documents/GitHub/LorenFranksDataMigration/src/test/datamigration/res/probe3.yml")
    ext = ElectrodeExtractor(prbs)
    trodes = ext.get_all_electrodes()
    print(trodes)
