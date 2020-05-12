from unittest import TestCase

from rec_to_nwb.processing.validation.not_empty_validator import NotEmptyValidator


class TestNotEmptyValidator(TestCase):

    def test_not_empty_validator_not_empty_string_valid(self):
        test_parameter = 'some not empty string'
        not_empty_validator = NotEmptyValidator(test_parameter)
        result = not_empty_validator.create_summary()
        self.assertTrue(result.is_valid)

    def test_not_empty_validator_empty_string_failed(self):
        test_parameter = ''
        not_empty_validator = NotEmptyValidator(test_parameter)
        result = not_empty_validator.create_summary()
        self.assertFalse(result.is_valid)
