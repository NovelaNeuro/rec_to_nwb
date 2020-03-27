class TaskNamesExtractor:

    def __init__(self, metadata):
        self.metadata = metadata

    def get_task_names(self):
        return [task_dict['task_name'] for task_dict in self.metadata['tasks']]

