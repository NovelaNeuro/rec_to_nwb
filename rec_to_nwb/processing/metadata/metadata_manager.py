
from rec_to_nwb.processing.metadata.metadata_extractor import MetadataExtractor
from rec_to_nwb.processing.nwb.components.device.probe.fl_probe_extractor import FlProbesExtractor
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.validation.metadata_validator import MetadataValidator
from rec_to_nwb.processing.validation.validation_registrator import ValidationRegistrator


class MetadataManager:
    """
    Args:
        metadata_path (string): path to file .yml with metadata describing experiment
        probes_paths (list of strings): list of paths to .yml files with data describing probes used in experiment
    """
    
    @beartype
    def __init__(self, metadata_path: str, probes_paths: list):
        self.__validate(metadata_path, probes_paths)

        self.probes_paths = probes_paths
        self.metadata_path = metadata_path

        self.fl_probes_extractor = FlProbesExtractor()
        self.metadata_extractor = MetadataExtractor()

        self.metadata = self.__get_metadata(metadata_path)
        self.probes = self.__get_probes(probes_paths)

    @staticmethod
    def __validate(metadata_path, probes_paths):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(MetadataValidator(metadata_path, probes_paths))
        validation_registrator.validate()

    def __get_metadata(self, metadata_path):
        return self.metadata_extractor.extract_metadata(metadata_path)

    def __get_probes(self, probes_paths):
        return self.fl_probes_extractor.extract_probes_metadata(probes_paths)

    def __str__(self):
        metadata_info = 'Experimenter: ' + self.metadata['experimenter name'] + \
                        '\nDescription: ' + self.metadata['experiment description'] + \
                        '\nSession Id: ' + self.metadata['session_id'] + \
                        '\nSubject: ' + self.metadata['subject']['description']

        probe_types = list(map(lambda probe: probe['probe_type'], self.probes))
        probe_types_info = '\n\nAvailable probe types: ' + str(probe_types)
        return 'Experiment Info:\n' + metadata_info + probe_types_info
