from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.validation.type_validation_summary import TypeValidationSummary
from fl.datamigration.validation.validator import Validator


class TypeValidator(Validator):

    def __init__(self, parameter, expected_type):
        self.parameter = parameter
        self.expected_type = expected_type

    def create_summary(self):
        if type(self.parameter) is None:
            raise NoneParamException("Parameter is None type")
        return TypeValidationSummary(self.parameter, self.expected_type)
