class ProbeInjector:

    def inject_all_probes(self, nwb_content, probes):
        for probe in probes.values():
            self.inject_probe(nwb_content, probe)

    @staticmethod
    def inject_probe(nwb_content, probe):
        nwb_content.add_device(probe)