from unittest import TestCase

from fl.datamigration.exceptions.missing_data_exception import MissingDataException
from fl.datamigration.tools.InputValidator import InputValidator
from pathlib import Path

path = Path(__file__).parent.parent
path.resolve()

class TestInputValidator(TestCase):
    def setUp(self):
        self.epochs = ['01_s1', '02_s1']
        self.animal = 'alien'
        self.date = '21251015'


    def test_validate_dataset(self):
        data_path = str(path) + '/res/scanner_test/'
        wrong_data_types_to_check = ['pos', 'non_existing']
        data_types_to_check = ['pos', 'mda']
        validator = InputValidator(data_types_to_check=data_types_to_check)
        wrong_data_validator = InputValidator(data_types_to_check=wrong_data_types_to_check)
        with self.assertRaises(MissingDataException):
            validator.validate_datasets_exist(data_path + 'non_existing_directory/',
                                              self.animal, self.date, self.epochs)
            wrong_data_validator.validate_datasets_exist(data_path, self.animal, self.date, self.epochs)
        pass
        self.assertEqual(validator.validate_datasets_exist(data_path, self.animal, self.date, self.epochs),
                         {'01_s1': {'pos': True, 'mda': True}, '02_s1': {'pos': True, 'mda': True}})

    def test_validate_metadata(self):
        validator = InputValidator(data_types_to_check=[])
        metadata_path = str(path) + '/res/metadata.yml'
        wrong_metadata_path = str(path) + '/res/metadataa.yml'
        probes_paths = [str(path) + '/res/probe1.yml',
                        str(path) + '/res/probe2.yml',
                        str(path) + '/res/probe3.yml']
        wrong_probes_paths = [str(path) + '/res/probe1.yml',
                              str(path) + '/res/probe2.yml',
                              str(path) + '/res/probe3.yml']
        with self.assertRaises(MissingDataException):
            validator.validate_metadata_exists(wrong_metadata_path, probes_paths)
            validator.validate_metadata_exists(metadata_path, wrong_probes_paths)
        pass
        self.assertIsNone(validator.validate_metadata_exists(metadata_path, probes_paths))


