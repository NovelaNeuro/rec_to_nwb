from unittest import TestCase

from fl.datamigration.validation.not_empty_validator import NotEmptyValidator


class TestNotEmptyValidator(TestCase):

    def test_not_empty_validator_not_empty_string_valid(self):
        test_parameter = 'some not empty string'
        not_empty_validator = NotEmptyValidator(test_parameter)
        result = not_empty_validator.createSummary()
        self.assertTrue(result.isValid())

    def test_not_empty_validator_empty_string_failed(self):
        test_parameter = ''
        not_empty_validator = NotEmptyValidator(test_parameter)
        result = not_empty_validator.createSummary()
        self.assertFalse(result.isValid())

