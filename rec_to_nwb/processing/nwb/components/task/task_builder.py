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

        # task_name_data = VectorData(
        #     name='task_name_data',
        #     description='None',
        #     data=task_name
        # )
        # task_name_index = VectorIndex(
        #     name='task_name_index',
        #     data=[id_counter for id_counter, _ in enumerate(task_name)],
        #     target=task_name_data
        # )
        # task_description_data = VectorData(
        #     name='task_description_data',
        #     description='None',
        #     data=task_description
        # )
        # task_description_index = VectorIndex(
        #     name='task_description_index',
        #     data=[id_counter for id_counter, _ in enumerate(task_description)],
        #     target=task_description_data
        # )
        # camera_id_data = VectorData(
        #     name='camera_id_data',
        #     description='None',
        #     data=camera_id
        # )
        # camera_id_index = VectorIndex(
        #     name='camera_id_index',
        #     data=[id_counter for id_counter, _ in enumerate(camera_id)],
        #     target=camera_id_data
        # )
        # task_epochs_data = VectorData(
        #     name='task_epochs_data',
        #     description='None',
        #     data=task_epochs
        # )
        # task_epochs_index = VectorIndex(
        #     name='task_description_index',
        #     data=[id_counter for id_counter, _ in enumerate(task_epochs)],
        #     target=task_epochs_data
        # )
        index = [id_counter for id_counter, _ in enumerate(task_name)]

        nwb_table = DynamicTable(
            name='task',
            description='None',
            id=index
        )

        nwb_table.add_column(
            name='task_name',
            description='None',
            data=task_name,
            index=index
        )
        nwb_table.add_column(
            name='task_description',
            description='None',
            data=task_description,
            index=index
        )
        nwb_table.add_column(
            name='camera_id',
            description='None',
            data=camera_id,
            index=index
        )
        nwb_table.add_column(
            name='task_epochs',
            description='None',
            data=task_epochs,
            index=index
        )

        return nwb_table
