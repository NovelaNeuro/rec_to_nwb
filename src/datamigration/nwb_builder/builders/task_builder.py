from hdmf.common import DynamicTable


def build_task(metadata, nwb_content):
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
    for task in metadata['tasks']:
        nwb_table.add_row(task)

    nwb_content.processing['behavior'].add_data_interface(nwb_table)