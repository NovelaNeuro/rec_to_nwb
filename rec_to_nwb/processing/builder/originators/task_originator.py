import logging.config
import os

from rec_to_nwb.processing.nwb.components.task.task_creator import TaskCreator
from rec_to_nwb.processing.nwb.components.task.task_manager import TaskManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TaskOriginator:
    def __init__(self, metadata):
        self.task_manager = TaskManager(metadata)

    def make(self, nwb_content):
        logger.info('Task: Building')
        fl_tasks = self.task_manager.get_fl_tasks()
        logger.info('Task: Creating')
        tasks = [
            TaskCreator.create(fl_task)
            for fl_task in fl_tasks
        ]
        logger.info('Task: Injecting into ProcessingModule')
        for task in tasks:
            nwb_content.processing['tasks'].add(task)
