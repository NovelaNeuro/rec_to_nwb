from src.datamigration.nwb.components.device.probe_extractor import ProbesExtractor
from src.datamigration.nwb_builder.extractors.metadata_extractor import MetadataExtractor


class MetadataManager:

    def __init__(self, metadata_path, probes_paths):
        self.probes_paths = probes_paths

        self.probes_extractor = ProbesExtractor()
        self.metadata_extractor = MetadataExtractor()

        self.metadata = self.__get_metadata(metadata_path)
        self.probes = self.__get_probes(probes_paths)

    def __get_metadata(self, metadata_path):
        return self.metadata_extractor.extract_metadata(metadata_path)

    def __get_probes(self, probes_paths):
        return self.probes_extractor.extract_probes_metadata(probes_paths)

    def __str__(self):
        metadata_info = 'Experimenter: ' + self.metadata['experimenter name'] + \
                        '\nDescription: ' + self.metadata['experiment description'] + \
                        '\nSession Id: ' + self.metadata['session_id'] + \
                        '\nStart Time: ' + self.metadata['session start time'] + \
                        '\nSubject: ' + self.metadata['subject']['description']

        probe_types = list(map(lambda probe: probe['probe_type'], self.probes))
        probe_types_info = '\n\nAvailable probe types: ' + str(probe_types)
        return 'Experiment Info:\n' + metadata_info + probe_types_info
