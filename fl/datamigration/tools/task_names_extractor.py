class TaskNamesExtractor:

    def __init__(self, tasks):
        self.tasks = tasks

    def get_task_names(self):
        return [task_dict['task_name'] for task_dict in self.tasks]

