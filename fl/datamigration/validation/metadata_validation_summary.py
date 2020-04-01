from fl.datamigration.validation.validation_summary import ValidationSummary


class MetadataValidationSummary(ValidationSummary):
    def __init__(self, missing_metadata):
        self.missing_metadata = missing_metadata

    def isValid(self):
        if not self.missing_metadata:
            return True
        else:
            return False
