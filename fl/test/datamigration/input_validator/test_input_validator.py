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


    def test_input_validator_validate_input_data_successfully(self):
        data_path = str(path) + '/res/scanner_test/'
        wrong_data_types_to_check = ['pos', 'non_existing']
        data_types_to_check = ['pos', 'mda']
        metadata_path = str(path) + '/res/metadata.yml'
        wrong_metadata_path = str(path) + '/res/metadataa.yml'
        probes_paths = [str(path) + '/res/probe1.yml',
                        str(path) + '/res/probe2.yml',
                        str(path) + '/res/probe3.yml']
        wrong_probes_paths = [str(path) + '/res/probe11.yml',
                              str(path) + '/res/probe22.yml',
                              str(path) + '/res/probe33.yml']
        validator = InputValidator()
        with self.assertRaises(MissingDataException):
            validator.validate_input_data(metadata_path,
                                          probes_paths,
                                          data_path + 'non_existing_directory/',
                                          self.animal,
                                          self.date,
                                          self.epochs,
                                          data_types_to_check)
        with self.assertRaises(MissingDataException):
            validator.validate_input_data(metadata_path,
                                          probes_paths,
                                          data_path,
                                          self.animal,
                                          self.date,
                                          self.epochs,
                                          wrong_data_types_to_check)
        with self.assertRaises(MissingDataException):
            validator.validate_input_data(metadata_path,
                                          wrong_probes_paths,
                                          data_path,
                                          self.animal,
                                          self.date,
                                          self.epochs,
                                          data_types_to_check)
        with self.assertRaises(MissingDataException):
            validator.validate_input_data(wrong_metadata_path,
                                          probes_paths,
                                          data_path,
                                          self.animal,
                                          self.date,
                                          self.epochs,
                                          data_types_to_check)


    def test_input_validator_validate_dataset_successfully(self):
        data_path = str(path) + '/res/scanner_test/'
        wrong_data_types_to_check = ['pos', 'non_existing']
        data_types_to_check = ['pos', 'mda']
        validator = InputValidator()
        self.assertEqual(validator.return_missing_data(data_path,
                                                       self.animal,
                                                       self.date,
                                                       self.epochs,
                                                       data_types_to_check),'')
        self.assertEqual(validator.return_missing_data(data_path,
                                                       self.animal,
                                                       self.date,
                                                       self.epochs,
                                                       wrong_data_types_to_check),
                         'non_existing files in epoch 01_s1\nnon_existing files in epoch 02_s1\n')

    def test_input_validator_validate_metadata_successfully(self):
        validator = InputValidator()
        metadata_path = str(path) + '/res/metadata.yml'
        wrong_metadata_path = str(path) + '/res/metadataa.yml'
        probes_paths = [str(path) + '/res/probe1.yml',
                        str(path) + '/res/probe2.yml',
                        str(path) + '/res/probe3.yml']
        wrong_probes_paths = [str(path) + '/res/probe11.yml',
                              str(path) + '/res/probe22.yml',
                              str(path) + '/res/probe33.yml']
        self.assertEqual(validator.return_missing_metadata(metadata_path, probes_paths), '')
        self.assertEqual(validator.return_missing_metadata(wrong_metadata_path, probes_paths),
                         str(path) + '/res/metadataa.yml\n')
        self.assertEqual(validator.return_missing_metadata(metadata_path, wrong_probes_paths),
                         str(path) + '/res/probe11.yml\n' +
                         str(path) + '/res/probe22.yml\n' +
                         str(path) + '/res/probe33.yml\n')


