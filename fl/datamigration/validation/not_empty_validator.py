from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.validation.not_empty_validation_summary import NotEmptyValidationSummary
from fl.datamigration.validation.validator import Validator


class NotEmptyValidator(Validator):

    def __init__(self, parameter):
        self.parameter = parameter

    def createSummary(self):
        if self.parameter is None:
            raise NoneParamException("Parameter is None type")
        return NotEmptyValidationSummary(self.parameter)
