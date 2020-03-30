import os
from unittest import TestCase

from fl.datamigration.exceptions.missing_data_exception import MissingDataException
from fl.datamigration.input_validator.input_validator import InputValidator
from pathlib import Path


path = Path(__file__).parent.parent
path.resolve()


class TestInputValidator(TestCase):
    def setUp(self):
        data_path = str(path) + '/res/scanner_test/'
        self.epochs = ['01_s1', '02_s1']
        animal = 'alien'
        date = '21251015'
        self.all_data = os.listdir(str(path) + '/res/scanner_test/alien/preprocessing/21251015')

    def test_input_validator_validate_input_data_successfully(self):
        wrong_data_types_to_check = ['pos', 'mda', 'non_existing']
        data_types_to_check = ['pos', 'mda']
        metadata_path = str(path) + '/res/metadata.yml'
        wrong_metadata_path = str(path) + '/res/metadataa.yml'
        probes_paths = [str(path) + '/res/probe1.yml',
                        str(path) + '/res/probe2.yml',
                        str(path) + '/res/probe3.yml']
        wrong_probes_paths = [str(path) + '/res/probe11.yml',
                              str(path) + '/res/probe22.yml',
                              str(path) + '/res/probe33.yml']
        validator_missing_type = InputValidator(metadata_path,
                                                probes_paths,
                                                self.all_data,
                                                self.epochs,
                                                wrong_data_types_to_check)
        validator_wrong_probes = InputValidator(metadata_path,
                                                wrong_probes_paths,
                                                self.all_data,
                                                self.epochs,
                                               data_types_to_check)
        validator_wrong_metadata = InputValidator(wrong_metadata_path,
                                                  probes_paths,
                                                  self.all_data,
                                                  self.epochs,
                                                  data_types_to_check)
        with self.assertRaises(MissingDataException):
            validator_missing_type.validate_input_data()
        with self.assertRaises(MissingDataException):
            validator_wrong_probes.validate_input_data()
        with self.assertRaises(MissingDataException):
            validator_wrong_metadata.validate_input_data()

