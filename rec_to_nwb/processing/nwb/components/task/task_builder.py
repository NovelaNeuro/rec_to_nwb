from hdmf.common import DynamicTable


class TaskBuilder:

    def __init__(self, metadata):
        self.metadata = metadata

    def build(self):
        if self.metadata is None:
            return None
        if self.metadata['tasks'] is None:
            return None
        if len(self.metadata['tasks']) == 0:
            return None
        return self.__build_tasks_dynamictable()

    def __build_tasks_dynamictable(self):
        task_name = []
        task_description = []
        camera_id = []
        task_epochs = []
        for task in self.metadata['tasks']:
            task_name.append(task['task_name'])
            task_description.append(task['task_description'])
            camera_id.append(task['camera_id'])
            task_epochs.append(task['task_epochs'])

        nwb_table = DynamicTable(
            name='task',
            description='None',
            id=[id_counter for id_counter, _ in enumerate(task_name)]
        )
        nwb_table.add_column(
            name='task_name',
            description='None',
            data=task_name,
        )
        nwb_table.add_column(
            name='task_description',
            description='None',
            data=task_description
        )
        nwb_table.add_column(
            name='camera_id',
            description='None',
            data=camera_id,
        )
        nwb_table.add_column(
            name='task_epochs',
            description='None',
            data=task_epochs,
        )

        return nwb_table
