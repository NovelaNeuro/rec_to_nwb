from fl.datamigration.validation.validation_summary import ValidationSummary


class TaskValidationSummary(ValidationSummary):

    def __init__(self, number_of_epochs, tasks):
        self.number_of_epochs = number_of_epochs
        self.tasks = tasks

    def isValid(self):
        number_of_epochs = self.number_of_epochs
        number_of_tasks = len(self.tasks)
        return number_of_epochs == number_of_tasks

