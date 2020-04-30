
from fl.datamigration.validation.validation_summary import ValidationSummary


class NotNoneValidationSummary(ValidationSummary):
    def is_valid(self):
        return True


