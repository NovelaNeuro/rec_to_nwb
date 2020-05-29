from rec_to_nwb.processing.validation.validation_summary import ValidationSummary


class MetadataValidationSummary(ValidationSummary):
    def __init__(self, missing_metadata):
        self.missing_metadata = missing_metadata

    def is_valid(self):
        return not bool(self.missing_metadata)
