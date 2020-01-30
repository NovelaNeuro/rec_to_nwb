import yaml

from src.datamigration.nwb_builder.extractors.probe_extractor import ProbesExtractor


class NWBMetadata:

    def __init__(self, metadata_path, probes_paths):
        with open(metadata_path, 'r') as stream:
            metadata_dict = yaml.safe_load(stream)
            self.metadata = metadata_dict
        self.probes = ProbesExtractor(probes_paths).probes_content
