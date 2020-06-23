
from rec_to_nwb.processing.nwb.components.task.fl_task import FlTask


class TaskBuilder:

    @staticmethod
    def build(name, description, task_name, task_description, camera_id, task_epochs):
        return FlTask(
            name=str(name),
            description=description,
            columns=[task_name, task_description, camera_id, task_epochs]
        )
