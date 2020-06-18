import logging.config
import os

from rec_to_nwb.processing.nwb.components.position.fl_position_manager import FlPositionManager
from rec_to_nwb.processing.nwb.components.position.position_creator import PositionCreator
from rec_to_nwb.processing.nwb.components.processing_module.processing_module_creator import ProcessingModuleCreator
from rec_to_nwb.processing.nwb.components.task.task_creator import TaskCreator
from rec_to_nwb.processing.nwb.components.task.task_manager import TaskManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ProcessingModuleOriginator:
    def __init__(self, datasets, metadata):
        self.task_manager = TaskManager(metadata)

        self.pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')
        self.fl_position_manager = FlPositionManager(datasets, float(metadata['meters_per_pixel']))
        self.position_creator = PositionCreator()

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
            self.pm_creator.insert(task)

        logger.info('Position: Building')
        fl_position = self.fl_position_manager.get_fl_position()
        logger.info('Position: Creating')
        position = self.position_creator.create(fl_position)
        logger.info('Position: Injecting into ProcessingModule')
        self.pm_creator.insert(position)

        nwb_content.add_processing_module(self.pm_creator.processing_module)
