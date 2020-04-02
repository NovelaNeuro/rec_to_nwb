from fl.datamigration.metadata.metadata_extractor import MetadataExtractor
from fl.datamigration.nwb.components.device.fl_probe_extractor import FlProbesExtractor
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none
from fl.datamigration.validation.metadata_validator import MetadataValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class MetadataManager:
    """
    Args:
        metadata_path (string): path to file .yml with metadata describing experiment
        probes_paths (list of strings): list of paths to .yml files with data describing probes used in experiment
    """
    def __init__(self, metadata_path, probes_paths):



        validate_parameters_not_none(__name__, metadata_path, probes_paths)

        validationRegistrator = ValidationRegistrator()
        validationRegistrator.register(MetadataValidator(metadata_path, probes_paths))
        validationRegistrator.validate()

        self.probes_paths = probes_paths
        self.metadata_path = metadata_path

        self.fl_probes_extractor = FlProbesExtractor()
        self.metadata_extractor = MetadataExtractor()

        self.metadata = self.__get_metadata(metadata_path)
        self.probes = self.__get_probes(probes_paths)

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
