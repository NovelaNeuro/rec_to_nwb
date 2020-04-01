from fl.datamigration.validation.validation_summary import ValidationSummary


class TypeValidationSummary(ValidationSummary):

    def __init__(self, parameter, expected_type):
        self.parameter = parameter
        self.expected_type = expected_type

    def isValid(self):
        return type(self.parameter) == self.expected_type

