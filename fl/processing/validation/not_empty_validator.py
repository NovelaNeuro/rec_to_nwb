from fl.processing.exceptions.none_param_exception import NoneParamException
from fl.processing.validation.not_empty_validation_summary import NotEmptyValidationSummary
from fl.processing.validation.validator import Validator


class NotEmptyValidator(Validator):

    def __init__(self, parameter):
        self.parameter = parameter

    def create_summary(self):
        if self.parameter is None:
            raise NoneParamException("Parameter is None type")
        return NotEmptyValidationSummary(self.parameter)
