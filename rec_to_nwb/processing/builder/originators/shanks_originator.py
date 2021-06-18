import os
import logging.config

from rec_to_nwb.processing.nwb.components.device.probe.shanks.fl_shank_manager import FlShankManager
from rec_to_nwb.processing.nwb.components.device.probe.shanks.shank_creator import ShankCreator

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ShanksOriginator:

    def __init__(self, probes, metadata):
        self.fl_shank_manager = FlShankManager(probes, metadata['electrode_groups'])
        self.shank_creator = ShankCreator()

    def make(self, shanks_electrodes_dict):
        logger.info('Probes-Shanks: Building')
        fl_shanks_dict = self.fl_shank_manager.get_fl_shanks_dict(shanks_electrodes_dict)
        logger.info('Probes-Shanks: Creating')
        shanks_dict = {}
        for probe_type, fl_shanks in fl_shanks_dict.items():
            shanks_dict[probe_type] = [self.shank_creator.create(fl_shank) for fl_shank in fl_shanks]
        return shanks_dict