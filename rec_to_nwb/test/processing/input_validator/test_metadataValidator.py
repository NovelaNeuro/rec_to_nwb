from pathlib import Path
from unittest import TestCase

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.validation.metadata_validator import MetadataValidator

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

        validator_summary = validator.create_summary()

        self.assertEqual(validator_summary.is_valid(), True)
        with self.assertRaises(MissingDataException):
            validator_wrong_metadata.create_summary()
        with self.assertRaises(MissingDataException):
            validator_wrong_probes.create_summary()
