from hdmf.common.table import VectorData
from rec_to_nwb.processing.nwb.components.task.task_builder import TaskBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import \
    validate_parameters_not_none


class TaskManager:

    @beartype
    def __init__(self, metadata: dict):
        self.metadata = metadata

        self.task_counter = 0

    def get_fl_tasks(self):
        validate_parameters_not_none(__name__, self.metadata['tasks'])

        return [
            self.__get_single_fl_task(
                task_name=task['task_name'],
                task_description=task['task_description'],
                camera_id=[int(camera_id) for camera_id in task['camera_id']],
                task_epochs=[int(epoch) for epoch in task['task_epochs']],
                task_environment=task['task_environment']
            )
            for task in self.metadata['tasks']
        ]

    def __get_single_fl_task(self, task_name, task_description, camera_id, task_epochs, task_environment):
        task_name_data = VectorData(
            name='task_name',
            description='the name of the task',
            data=[task_name]
        )
        task_description_data = VectorData(
            name='task_description',
            description='a description of the task',
            data=[task_description]
        )
        camera_id_data = VectorData(
            name='camera_id',
            description='the ID number of the camera used for video',
            data=[camera_id]
        )
        task_epochs_data = VectorData(
            name='task_epochs',
            description='the temporal epochs where the animal was exposed to this task',
            data=[task_epochs]
        )
        environment_data = VectorData(
            name='task_environment',
            description='the environment in which the animal performed the task',
            data=[task_environment]
        )

        task = TaskBuilder.build(
            name='task_' + str(self.task_counter),
            description='',
            task_name=task_name_data,
            task_description=task_description_data,
            camera_id=camera_id_data,
            task_epochs=task_epochs_data,
            task_environment=environment_data
        )
        self.task_counter += 1

        return task
