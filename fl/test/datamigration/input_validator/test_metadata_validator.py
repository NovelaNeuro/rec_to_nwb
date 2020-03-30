from unittest import TestCase

from pathlib import Path

from fl.datamigration.input_validator.metadata_validator import MetadataValidator

path = Path(__file__).parent.parent
path.resolve()


class TestInputValidator(TestCase):
    def setUp(self):
        self.metadata_path = str(path) + '/res/metadata.yml'
        self.wrong_metadata_path = str(path) + '/res/metadataa.yml'
        self.probes_paths = [str(path) + '/res/probe1.yml',
                        str(path) + '/res/probe2.yml',
                        str(path) + '/res/probe3.yml']
        self.wrong_probes_paths = [str(path) + '/res/probe11.yml',
                              str(path) + '/res/probe22.yml',
                              str(path) + '/res/probe33.yml']

    def test_input_validator_validate_metadata_successfully(self):
        validator = MetadataValidator(self.metadata_path, self.probes_paths)
        validator_wrong_metadata = MetadataValidator(self.wrong_metadata_path, self.probes_paths)
        validator_wrong_probes = MetadataValidator(self.metadata_path, self.wrong_probes_paths)
        self.assertEqual(validator.get_missing_metadata(), [])
        self.assertEqual(validator_wrong_metadata.get_missing_metadata(),[str(path) + '/res/metadataa.yml'])
        self.assertEqual(validator_wrong_probes.get_missing_metadata(),
                         [str(path) + '/res/probe11.yml',
                          str(path) + '/res/probe22.yml',
                          str(path) + '/res/probe33.yml'])
