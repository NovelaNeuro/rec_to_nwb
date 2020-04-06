from fl.datamigration.validation.validation_summary import ValidationSummary


class TaskValidationSummary(ValidationSummary):

    def __init__(self, tasks):
        self.tasks = tasks

    def isValid(self):
        return type(self.tasks) == list

