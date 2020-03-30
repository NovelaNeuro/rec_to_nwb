import os
from unittest import TestCase

from pathlib import Path

from fl.datamigration.input_validator.preprocessing_validator import PreprocessingValidator


path = Path(__file__).parent.parent
path.resolve()


class TestInputValidator(TestCase):
    def setUp(self):
        self.data_path = str(path) + '/res/scanner_test/'
        self.epochs = ['01_s1', '02_s1']
        self.animal = 'alien'
        self.date = '21251015'
        self.all_data = os.listdir(str(path) + '/res/scanner_test/alien/preprocessing/21251015')

    def test_input_validator_validate_dataset_successfully(self):
        wrong_data_types_to_check = ['pos', 'mda', 'non_existing']
        data_types_to_check = ['pos', 'mda']

        validator = PreprocessingValidator(self.all_data,
                                           self.epochs,
                                           data_types_to_check)
        validator_missing_type = PreprocessingValidator(self.all_data,
                                                        self.epochs,
                                                        wrong_data_types_to_check)

        self.assertEqual(validator.get_missing_preprocessing_data(), [])
        self.assertEqual(validator_missing_type.get_missing_preprocessing_data(),
                         [('non_existing', '01_s1'), ('non_existing', '02_s1')])




