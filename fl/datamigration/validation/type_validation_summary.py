from fl.datamigration.exceptions.incorrect_type_exception import IncorrectTypeException
from fl.datamigration.validation.validation_summary import ValidationSummary


class TypeValidationSummary(ValidationSummary):

    def __init__(self, parameter, expected_type):
        self.parameter = parameter
        self.expected_type = expected_type

    def is_valid(self):
        if not isinstance(self.parameter, self.expected_type):
            raise IncorrectTypeException(self.parameter, self.expected_type)
        return isinstance(self.parameter, self.expected_type)

