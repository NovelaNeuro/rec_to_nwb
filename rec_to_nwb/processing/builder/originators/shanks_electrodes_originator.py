import logging.config
import os

from rec_to_nwb.processing.nwb.components.device.probe.shanks_electrodes.fl_shanks_electrode_manager import \
    FlShanksElectrodeManager
from rec_to_nwb.processing.nwb.components.device.probe.shanks_electrodes.shanks_electrode_creator import \
    ShanksElectrodeCreator

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ShanksElectrodeOriginator:

    def __init__(self, probes, metadata):
        self.fl_shanks_electrode_manager = FlShanksElectrodeManager(probes, metadata['electrode_groups'])
        self.shanks_electrodes_creator = ShanksElectrodeCreator()

    def make(self):
        logger.info('Probes-ShanksElectrode: Building')
        fl_shanks_electrodes_dict = self.fl_shanks_electrode_manager.get_fl_shanks_electrodes_dict()
        logger.info('Probes-ShanksElectrode: Creating')
        shanks_electrodes_dict = {}
        for probe_type, fl_shanks_electrodes in fl_shanks_electrodes_dict.items():
            shanks_electrodes_dict[probe_type] = [
                self.shanks_electrodes_creator.create(fl_shanks_electrode)
                for fl_shanks_electrode in fl_shanks_electrodes
            ]
        return shanks_electrodes_dict
