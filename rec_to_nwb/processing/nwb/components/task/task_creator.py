from hdmf.common.table import DynamicTable
from rec_to_nwb.processing.nwb.components.task.fl_task import FlTask
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class TaskCreator:

    @classmethod
    @beartype
    def create(cls, fl_task: FlTask):
        return DynamicTable(
            name=fl_task.name,
            description=fl_task.description,
            columns=fl_task.columns,
        )
