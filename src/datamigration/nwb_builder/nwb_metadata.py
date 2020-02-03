import yaml

from src.datamigration.nwb_builder.extractors.probe_extractor import ProbesExtractor


class NWBMetadata:

    def __init__(self, metadata_path, probes_paths):
        with open(metadata_path, 'r') as stream:
            self.metadata = yaml.safe_load(stream)
        probes_extractor = ProbesExtractor()
        probes_extractor.extract_probes_metadata(probes_paths)
        self.probes = probes_extractor.probes_content

    def __str__(self):
        metadata_info = 'Experimenter: ' + self.metadata['experimenter name'] + \
                        '\nDescription: ' + self.metadata['experiment description'] + \
                        '\nSession Id: ' + self.metadata['session_id'] + \
                        '\nStart Time: ' + self.metadata['session start time'] + \
                        '\nSubject: ' + self.metadata['subject']['description']

        probe_types = list(map(lambda probe: probe['probe_type'], self.probes))
        probe_types_info = '\n\nAvailable probe types: ' + str(probe_types)
        return 'Experiment Info:\n' + metadata_info + probe_types_info
