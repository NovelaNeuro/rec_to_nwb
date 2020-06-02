import os
import logging.config

from rec_to_nwb.processing.nwb.components.mda.time.invalid.fl_mda_invalid_time_manager import FlMdaInvalidTimeManager
from rec_to_nwb.processing.nwb.components.mda.time.invalid.mda_invalid_time_injector import MdaInvalidTimeInjector

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaInvalidTimeOriginator:

    def __init__(self, header):
        self.fl_mda_invalid_time_manager = FlMdaInvalidTimeManager(
            sampling_rate=float(header.configuration.hardware_configuration.sampling_rate),
        )
        self.mda_invalid_time_injector = MdaInvalidTimeInjector()

    def make(self, nwb_content):
        logger.info('MDA invalid times: Building')
        mda_invalid_times = self.fl_mda_invalid_time_manager.get_fl_mda_invalid_times(nwb_content)
        logger.info('MDA invalid times: Injecting')
        self.mda_invalid_time_injector.inject_all(mda_invalid_times, nwb_content)
