from unittest import TestCase

from pathlib import Path

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.validation.preprocessing_validator import PreprocessingValidator

path = Path(__file__).parent.parent
path.resolve()


class TestInputValidator(TestCase):
    def setUp(self):
        self.data_path = str(path) + '/res/scanner_test/'
        self.epochs = ['01_s1', '02_s1']
        self.animal = 'alien'
        self.date = '21251015'

    def test_input_validator_validate_dataset_successfully(self):
        wrong_data_types_to_check = {'pos': True, 'mda': True, 'non_existing': True}
        data_types_to_check = {'pos': True, 'mda': True, 'non_existing': False}

        validator = PreprocessingValidator(str(path) + '/res/scanner_test/alien/preprocessing/21251015',
                                           self.epochs,
                                           data_types_to_check)
        validator_missing_type = PreprocessingValidator(str(path) + '/res/scanner_test/alien/preprocessing/21251015',
                                                        self.epochs,
                                                        wrong_data_types_to_check)

        self.assertEqual(validator.create_summary().is_valid(), True)
        with self.assertRaises(MissingDataException):
            validator_missing_type.create_summary()




