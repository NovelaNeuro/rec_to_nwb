from src.datamigration.nwb_builder.creators.probe_creator import ProbeCreator
from src.datamigration.nwb_builder.extractors.probe_extractor import ProbesExtractor


class ProbeBuilder:
    def __init__(self, probes_paths):
        self.probe_extractor = ProbesExtractor()
        self.probe_extractor.extract_probes_metadata(probes_paths)
        self.probe_creator = ProbeCreator()

    def build(self, electrode_groups_metadata):
        probes = {}
        for probe_counter, electrode_group_metadata in enumerate(electrode_groups_metadata):
            probe_metadata = self.probe_extractor.get_probe_file(electrode_group_metadata['device_type'])
            probes[probe_counter] = self.probe_creator.create_probe(probe_metadata, probe_counter)
        return probes