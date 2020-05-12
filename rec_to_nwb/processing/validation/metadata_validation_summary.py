from rec_to_nwb.processing.validation.validation_summary import ValidationSummary


class MetadataValidationSummary(ValidationSummary):
    def __init__(self, missing_metadata):
        self.missing_metadata = missing_metadata

    @property
    def is_valid(self):
        if not self.missing_metadata:
            return True
        return False
