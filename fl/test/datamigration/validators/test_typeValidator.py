from unittest import TestCase

from testfixtures import should_raise

from fl.datamigration.exceptions.incorrect_type_exception import IncorrectTypeException
from fl.datamigration.validation.type_validator import TypeValidator


class TestTypeValidator(TestCase):

    def test_type_validator_string_type_valid(self):
        test_parameter = 'test_string_parameter'
        type_validator = TypeValidator(test_parameter, str)
        result = type_validator.createSummary()
        self.assertTrue(result.isValid())

    @should_raise(IncorrectTypeException)
    def test_type_validator_different_type_failed(self):
        test_parameter = 44
        type_validator = TypeValidator(test_parameter, dict)
        result = type_validator.createSummary()
        self.assertFalse(result.isValid())

