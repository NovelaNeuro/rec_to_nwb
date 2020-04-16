
from fl.datamigration.validation.validation_summary import ValidationSummary


class NotNoneValidationSummary(ValidationSummary):
    def isValid(self):
            return True


