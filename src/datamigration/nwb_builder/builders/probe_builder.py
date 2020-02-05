from src.datamigration.nwb_builder.creators.probe_creator import ProbeCreator
from src.datamigration.nwb_builder.extractors.probe_extractor import ProbesExtractor


class ProbesDictBuilder:
    def __init__(self, probes_metadata):
        self.probe_extractor = ProbesExtractor()
        self.probe_creator = ProbeCreator()
        self.probes_metadata = probes_metadata

    def build(self, electrode_groups_metadata):
        probes = {}
        for probe_counter, electrode_group_metadata in enumerate(electrode_groups_metadata):
            probes[probe_counter] = self.build_single_probe(electrode_group_metadata, probe_counter, probes)
        return probes

    def build_single_probe(self, electrode_group_metadata, probe_counter, probes):
        probe_metadata = self.probe_extractor.filtr_by_type(self.probes_metadata,
                                                            electrode_group_metadata['device_type'])
        return self.probe_creator.create_probe(probe_metadata, probe_counter)
