class TaskValidator:

    def __init__(self, datasets, metadata):
        self.datasets = datasets
        self.metadata = metadata

    def is_number_of_tasks_valid(self):
        number_of_epochs = len(self.datasets)
        number_of_tasks = len(self.metadata['tasks'])
        return number_of_epochs == number_of_tasks