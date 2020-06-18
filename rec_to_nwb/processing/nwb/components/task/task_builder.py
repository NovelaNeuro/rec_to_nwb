from rec_to_nwb.processing.nwb.components.task.fl_task import FlTask


class TaskBuilder:

    @staticmethod
    def build(name, description, task_name, task_description, camera_id, task_epochs):
        return FlTask(
            name=name,
            description=description,
            columns=[task_name, task_description, camera_id, task_epochs]
        )
        nwb_table.add_column(
            name='task_description',
            description='None',
        )
        nwb_table.add_column(
            name='camera_id',
            description='None',
        )
        nwb_table.add_column(
            name='task_epochs',
            description='None',
        )
        for task in self.metadata['tasks']:
            nwb_table.add_row(task)
        return nwb_table
