class TaskValidator:

    def __init__(self, datasets, tasks):
        self.datasets = datasets
        self.tasks = tasks

    def is_number_of_tasks_valid(self):
        number_of_epochs = len(self.datasets)
        number_of_tasks = len(self.tasks)
        return number_of_epochs == number_of_tasks
