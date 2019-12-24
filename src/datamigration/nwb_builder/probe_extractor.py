from src.datamigration.probe.probe import Probe


class ProbeExtractor:

    def __init__(self, probe_path):
        self.probe = Probe(probe_path)
