from fldatamigration.processing.validation.validator import Validator
from fldatamigration.processing.exceptions.invalid_input_exception import InvalidInputException


class ValidationRegistrator(Validator):

    def __init__(self):
        self.validators = []

    def register(self, validator):
        if isinstance(validator, Validator):
            self.validators.append(validator)

    def validate(self):
        for validator in self.validators:
            result = validator.create_summary()
            if not result.is_valid():
                raise InvalidInputException("Validation: " + str(type(validator)) + "has failed!")
