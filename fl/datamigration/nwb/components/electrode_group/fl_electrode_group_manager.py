from fl.datamigration.nwb.components.electrode_group.fl_electrode_group import FlElectrodeGroup
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlElectrodeGroupManager:

    def __init__(self, electrode_groups_metadata):
        self.electrode_groups_metadata = electrode_groups_metadata

    def get_fl_electrode_groups(self, probes):
        validate_parameters_not_none(__name__, self.electrode_groups_metadata, probes)

        return [FlElectrodeGroup(
            metadata=electrode_group_metadata,
            device=probes[counter]
        ) for counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata)]
