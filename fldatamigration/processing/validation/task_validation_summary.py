from fldatamigration.processing.validation.validation_summary import ValidationSummary


class TaskValidationSummary(ValidationSummary):

    def __init__(self, tasks):
        self.tasks = tasks

    def is_valid(self):
        return isinstance(self.tasks, list)

