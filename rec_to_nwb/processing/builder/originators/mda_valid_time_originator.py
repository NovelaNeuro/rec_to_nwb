import os
import logging.config

from rec_to_nwb.processing.nwb.components.mda.time.valid.fl_mda_valid_time_manager import FlMdaValidTimeManager
from rec_to_nwb.processing.nwb.components.mda.time.valid.mda_valid_time_injector import MdaValidTimeInjector

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaValidTimeOriginator:

    def __init__(self, header):
        self.fl_mda_valid_time_manager = FlMdaValidTimeManager(
            sampling_rate=float(header.configuration.hardware_configuration.sampling_rate),
        )
        self.mda_valid_time_injector = MdaValidTimeInjector()

    def make(self, nwb_content):
        logger.info('MDA valid times: Building')
        mda_valid_times = self.fl_mda_valid_time_manager.get_fl_mda_valid_times(nwb_content)
        logger.info('MDA valid times: Injecting')
        self.mda_valid_time_injector.inject_all(mda_valid_times, nwb_content)
