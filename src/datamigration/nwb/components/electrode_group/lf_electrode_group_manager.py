from src.datamigration.nwb.components.electrode_group.fl_electrode_group_creator import FlElectrodeGroupCreator
from src.datamigration.nwb.components.electrode_group.lf_fl_electrode_group import LfFLElectrodeGroup


class FlElectrodeGroupManager:

    def __init__(self, electrode_groups_metadata):
        self.electrode_groups_metadata = electrode_groups_metadata

    def get_lf_fl_electrode_groups(self, probes):
        return [LfFLElectrodeGroup(
            metadata=electrode_group_metadata,
            device=probes[counter]
        ) for counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata)]
