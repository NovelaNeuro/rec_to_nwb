import logging.config
import os

from rec_to_nwb.processing.nwb.components.position.time.invalid.fl_pos_invalid_time_manager import \
    FlPosInvalidTimeManager
from rec_to_nwb.processing.nwb.components.position.time.invalid.pos_invalid_time_injector import \
    PosInvalidTimeInjector

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PosInvalidTimeOriginator:

    def __init__(self, metadata):
        self.fl_pos_invalid_time_manager = FlPosInvalidTimeManager(metadata)
        self.pos_invalid_time_injector = PosInvalidTimeInjector()

    def make(self, nwb_content):
        logger.info('POS invalid times: Building')
        pos_invalid_times = self.fl_pos_invalid_time_manager.get_fl_pos_invalid_times(
            nwb_content)
        logger.info('POS invalid times: Injecting')
        self.pos_invalid_time_injector.inject_all(
            pos_invalid_times, nwb_content)
