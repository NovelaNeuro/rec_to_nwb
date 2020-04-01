from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.validation.type_validation_summary import TypeValidationSummary
from fl.datamigration.validation.validator import Validator


class TypeValidator(Validator):

    def __init__(self, class_name, expected_type, parameter):
        self.class_name = class_name
        self.expected_type = expected_type
        self.parameter = parameter

    def createSummary(self):
        if type(self.parameter) is None:
            raise NoneParamException(self.class_name, self.parameter)
        return TypeValidationSummary(self.parameter, self.expected_type)
