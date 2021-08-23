from rec_to_nwb.processing.validation.validation_summary import \
    ValidationSummary


class AssociatedFilesValidationSummary(ValidationSummary):

    def __init__(self, associated_files):
        self.associated_files = associated_files

    def is_valid(self):
        return isinstance(self.associated_files, list)
