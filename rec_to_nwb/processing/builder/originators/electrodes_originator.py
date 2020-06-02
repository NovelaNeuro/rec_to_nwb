import os
import logging.config

from rec_to_nwb.processing.nwb.components.electrodes.electrode_creator import ElectrodesCreator
from rec_to_nwb.processing.nwb.components.electrodes.fl_electrode_manager import FlElectrodeManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodesOriginator:

    def __init__(self, probes, metadata):
        self.fl_electrode_manager = FlElectrodeManager(probes, metadata['electrode groups'])
        self.electrode_creator = ElectrodesCreator()

    def make(self, nwb_content, electrode_groups, electrodes_valid_map, electrode_groups_valid_map):
        logger.info('Electrodes: Building')
        fl_electrodes = self.fl_electrode_manager.get_fl_electrodes(
            electrode_groups=electrode_groups,
            electrodes_valid_map=electrodes_valid_map,
            electrode_groups_valid_map=electrode_groups_valid_map
        )
        logger.info('Electrodes: Creating&Injecting into NWB')
        [self.electrode_creator.create(nwb_content, fl_electrode) for fl_electrode in fl_electrodes]
