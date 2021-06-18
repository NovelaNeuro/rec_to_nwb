import os
import logging.config

from rec_to_nwb.processing.nwb.components.electrode_group.electrode_group_factory import ElectrodeGroupFactory
from rec_to_nwb.processing.nwb.components.electrode_group.electrode_group_injector import ElectrodeGroupInjector
from rec_to_nwb.processing.nwb.components.electrode_group.fl_nwb_electrode_group_manager import \
    FlNwbElectrodeGroupManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodeGroupOriginator:

    def __init__(self, metadata):
        self.fl_nwb_electrode_group_manager = FlNwbElectrodeGroupManager(metadata['electrode_groups'])
        self.electrode_group_creator = ElectrodeGroupFactory()
        self.electrode_group_injector = ElectrodeGroupInjector()

    def make(self, nwb_content, probes, electrode_groups_valid_map):
        logger.info('ElectrodeGroups: Building')
        fl_nwb_electrode_groups = self.fl_nwb_electrode_group_manager.get_fl_nwb_electrode_groups(
            probes=probes,
            electrode_groups_valid_map=electrode_groups_valid_map
        )
        logger.info('ElectrodeGroups: Creating')
        nwb_electrode_groups = [
            self.electrode_group_creator.create_nwb_electrode_group(nwb_electrode_group)
            for nwb_electrode_group in fl_nwb_electrode_groups
        ]
        logger.info('ElectrodeGroups: Injecting into NWB')
        self.electrode_group_injector.inject_all_electrode_groups(nwb_content, nwb_electrode_groups)
        return nwb_electrode_groups
