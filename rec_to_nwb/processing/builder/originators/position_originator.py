import logging.config
import os

from pynwb import NWBFile

from rec_to_nwb.processing.nwb.components.position.fl_position_manager import FlPositionManager
from rec_to_nwb.processing.nwb.components.position.position_creator import PositionCreator
from rec_to_nwb.processing.nwb.components.processing_module.processing_module_creator import ProcessingModuleCreator
from rec_to_nwb.processing.tools.beartype.beartype import beartype

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PositionOriginator:

    @beartype
    def __init__(self, datasets: list, metadata: dict, dataset_names: list,
                    process_timestamps: bool,
                    convert_timestamps: bool = True):
        self.pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')
        self.fl_position_manager = FlPositionManager(datasets, metadata, dataset_names, process_timestamps,
                                                    convert_timestamps=convert_timestamps)
        self.position_creator = PositionCreator()

    @beartype
    def make(self, nwb_content: NWBFile):
        logger.info('Position: Building')
        fl_positions = self.fl_position_manager.get_fl_positions()
        logger.info('Position: Creating')
        position = self.position_creator.create_all(fl_positions)
        logger.info('Position: Injecting into ProcessingModule')
        nwb_content.processing['behavior'].add(position)
