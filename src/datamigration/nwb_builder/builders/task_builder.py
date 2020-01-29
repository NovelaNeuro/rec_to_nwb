from hdmf.common import DynamicTable


class TaskBuilder:

    def __init__(self, metadata):
        self.metadata = metadata

    def build(self):
        nwb_table = DynamicTable(
            name='task',
            description='None',
        )

        nwb_table.add_column(
            name='task_name',
            description='None',
        )
        nwb_table.add_column(
            name='task_description',
            description='None',
        )
        for task in self.metadata['tasks']:
            nwb_table.add_row(task)

        return nwb_table
