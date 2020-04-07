from fl.datamigration.validation.validation_summary import ValidationSummary


class EqualLengthValidationSummary(ValidationSummary):
    def isValid(self):
        return True