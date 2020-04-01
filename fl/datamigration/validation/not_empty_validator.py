from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.validation.not_empty_validation_summary import NotEmptyValidationSummary
from fl.datamigration.validation.validator import Validator


class NotEmptyValidator(Validator):

    def __init__(self, class_name, parameter, parameter_name):
        super().__init__()
        self.class_name = class_name
        self.parameter = parameter
        self.parameter_name = parameter_name

    def createSummary(self):
        if self.parameter is None:
            raise NoneParamException("Parameter is None type")
        return NotEmptyValidationSummary(self.parameter)
