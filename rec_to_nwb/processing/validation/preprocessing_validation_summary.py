from rec_to_nwb.processing.validation.validation_summary import ValidationSummary


class PreprocessingValidationSummary(ValidationSummary):

    def __init__(self, missing_preprocessing_data):
        self.missing_preprocessing_data = missing_preprocessing_data

    def is_valid(self):
        return not self.missing_preprocessing_data
