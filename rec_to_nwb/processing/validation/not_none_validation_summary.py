
from rec_to_nwb.processing.validation.validation_summary import ValidationSummary


class NotNoneValidationSummary(ValidationSummary):
    def is_valid(self):
        return True


