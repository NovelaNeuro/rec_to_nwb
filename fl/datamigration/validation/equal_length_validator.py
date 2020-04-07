from fl.datamigration.exceptions.not_equal_param_length_exception import NotEqualParamLengthException
from fl.datamigration.validation.equal_length_validation_summary import EqualLengthValidationSummary
from fl.datamigration.validation.validator import Validator


class EqualLengthValidator(Validator):
    def __init__(self, parameters):
        self.parameters = parameters

    def createSummary(self):
        previous_parameter = self.parameters[0]
        for parameter in self.parameters:
            if len(parameter) != len(previous_parameter):
                raise NotEqualParamLengthException('Parameters lengths are not equal')
            previous_parameter = parameter
        return EqualLengthValidationSummary()