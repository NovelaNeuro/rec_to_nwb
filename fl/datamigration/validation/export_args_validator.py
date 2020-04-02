from fl.datamigration.exceptions.invalid_input_exception import InvalidInputException
from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.validation.export_args_validation_summary import ExportArgsValidationSummary
from fl.datamigration.validation.validator import Validator


class ExportArgsValidator(Validator):
    def __init__(self, export_args):
        self.export_args = export_args

    def createSummary(self):
        if not self.export_args:
            raise NoneParamException()
        if not type(self.export_args) == tuple:
            raise InvalidInputException("Export args are not tuple")
        for single_value in self.export_args:
            if not type(single_value) == str:
                raise InvalidInputException("One or more values in export args are not strings")
        return ExportArgsValidationSummary()
