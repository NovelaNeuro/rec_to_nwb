from fl.datamigration.validation.validation_summary import ValidationSummary


class TaskValidationSummary(ValidationSummary):

    def __init__(self, number_of_datasets, tasks):
        self.number_of_datasets = number_of_datasets
        self.tasks = tasks

    def isValid(self):
        number_of_epochs = self.number_of_datasets
        number_of_tasks = len(self.tasks)
        return number_of_epochs == number_of_tasks

