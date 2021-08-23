import logging.config
import os

from rec_to_nwb.processing.nwb.components.position.time.valid.fl_pos_valid_time_manager import \
    FlPosValidTimeManager
from rec_to_nwb.processing.nwb.components.position.time.valid.pos_valid_time_injector import \
    PosValidTimeInjector

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PosValidTimeOriginator:

    def __init__(self, metadata):
        self.fl_pos_valid_time_manager = FlPosValidTimeManager(metadata)
        self.pos_valid_time_injector = PosValidTimeInjector()

    def make(self, nwb_content):
        logger.info('POS valid times: Building')
        pos_valid_times = self.fl_pos_valid_time_manager.get_fl_pos_valid_times(
            nwb_content)
        logger.info('POS valid times: Injecting')
        self.pos_valid_time_injector.inject_all(pos_valid_times, nwb_content)
