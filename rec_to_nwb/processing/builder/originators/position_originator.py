import logging.config
import os

from rec_to_nwb.processing.nwb.components.position.fl_position_manager import FlPositionManager
from rec_to_nwb.processing.nwb.components.position.position_creator import PositionCreator
from rec_to_nwb.processing.nwb.components.processing_module.processing_module_creator import ProcessingModuleCreator

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PositionOriginator:
    def __init__(self, datasets, metadata):
        self.pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')
        self.fl_position_manager = FlPositionManager(datasets, float(metadata['meters_per_pixel']))
        self.position_creator = PositionCreator()

    def make(self, nwb_content):
        logger.info('Position: Building')
        fl_position = self.fl_position_manager.get_fl_position()
        logger.info('Position: Creating')
        position = self.position_creator.create(fl_position)
        logger.info('Position: Injecting into ProcessingModule')
        nwb_content.processing['behavior'].add(position)
