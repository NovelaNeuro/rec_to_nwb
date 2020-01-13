from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_builder.probe_extractor import ProbesExtractor


class NWBMetadata:

    def __init__(self, metadata_path, probes_paths):
        self.metadata = MetadataExtractor(metadata_path)
        self.probes = ProbesExtractor(probes_paths).probes_content
