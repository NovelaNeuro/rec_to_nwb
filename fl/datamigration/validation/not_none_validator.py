from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.validation.not_none_validation_summary import NotNoneValidationSummary
from fl.datamigration.validation.validator import Validator


class NotNoneValidator(Validator):
    def __init__(self, parameter):
        self.parameter = parameter

    def createSummary(self):
        if self.parameter == None:
            raise NoneParamException("parameter is None")
        return NotNoneValidationSummary()