from fl.datamigration.validation.validator import Validator
from fl.datamigration.exceptions.invalid_input_exception import InvalidInputException


class ValidationRegistrator(Validator):

    def __init__(self):
        self.validators = []

    def register(self, validator):
        if (type(validator) == Validator):
            self.validators.append(validator)

    def validate(self):
        for validator in self.validators:
            result = validator.createSummary()
            if not result.isValid():
                raise InvalidInputException("Validation: " + str(type(validator) + "has failed!"))
