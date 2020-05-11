from rec_to_nwb.processing.exceptions.none_param_exception import NoneParamException
from rec_to_nwb.processing.validation.not_none_validation_summary import NotNoneValidationSummary
from rec_to_nwb.processing.validation.validator import Validator


class NotNoneValidator(Validator):

    def __init__(self, parameter):
        self.parameter = parameter

    def create_summary(self):
        if self.parameter is None:
            raise NoneParamException("Parameter is None type")
        return NotNoneValidationSummary()
