import logging.config
import os

from hdmf.common import DynamicTable

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


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
