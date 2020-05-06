from fl.processing.exceptions.none_param_exception import NoneParamException
from fl.processing.validation.not_none_validation_summary import NotNoneValidationSummary
from fl.processing.validation.validator import Validator


class NotNoneValidator(Validator):

    def __init__(self, parameter):
        self.parameter = parameter

    def create_summary(self):
        if self.parameter is None:
            raise NoneParamException("Parameter is None type")
        return NotNoneValidationSummary()
