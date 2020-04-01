from unittest import TestCase

from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.tools.name_extractor import NameExtractor
from fl.datamigration.validation.type_validator import TypeValidator


def test_function(test_parameter):
    return test_parameter

class TestTypeValidator(TestCase):

    def test_type_validator_string_type_valid(self):
        test_parameter = 'test_string_parameter'
        type_validator = TypeValidator(__name__, test_parameter, NameExtractor.extract_name(test_function)[0], str)
        result = type_validator.createSummary()
        self.assertTrue(result.isValid())

    def test_type_validator_different_type_failed(self):
        test_parameter = 44
        type_validator = TypeValidator(__name__, test_parameter, NameExtractor.extract_name(test_function)[0], dict)
        result = type_validator.createSummary()
        self.assertFalse(result.isValid())

    @should_raise(NoneParamException)
    def test_type_validator_different_type_raise_NoneParamException(self):
        test_parameter = None
        type_validator = TypeValidator(__name__, test_parameter, NameExtractor.extract_name(test_function)[0], dict)
        type_validator.createSummary()
