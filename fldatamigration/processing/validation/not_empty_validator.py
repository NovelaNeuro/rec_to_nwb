from fldatamigration.processing.exceptions.none_param_exception import NoneParamException
from fldatamigration.processing.validation.not_empty_validation_summary import NotEmptyValidationSummary
from fldatamigration.processing.validation.validator import Validator


class NotEmptyValidator(Validator):

    def __init__(self, parameter):
        self.parameter = parameter

    def create_summary(self):
        if self.parameter is None:
            raise NoneParamException("Parameter is None type")
        return NotEmptyValidationSummary(self.parameter)
