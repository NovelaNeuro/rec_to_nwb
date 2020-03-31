from fl.datamigration.validation.validation_summary import ValidationSummary


class PreprocessingValidationSummary(ValidationSummary):
    def __init__(self, missing_preprocessing_data):
        self.missing_preprocessing_data = missing_preprocessing_data

    def isValid(self):
        if self.missing_preprocessing_data == []:
            return True
        else:
            return False
