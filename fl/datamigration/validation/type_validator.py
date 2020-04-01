from fl.datamigration.tools.validate_parameters import validate_parameters_not_none
from fl.datamigration.validation.type_validation_summary import TypeValidationSummary
from fl.datamigration.validation.validator import Validator


class TypeValidator(Validator):

    def __init__(self, class_name, parameter, parameter_name, expected_type):
        super().__init__()
        self.class_name = class_name
        self.parameter = parameter
        self.parameter_name = parameter_name
        self.expected_type = expected_type

    def createSummary(self):
        validate_parameters_not_none(self.class_name, [self.parameter], [self.parameter_name])
        return TypeValidationSummary(self.parameter, self.expected_type)
