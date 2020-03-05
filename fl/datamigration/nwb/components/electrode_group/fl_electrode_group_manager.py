from fl.datamigration.nwb.components.electrode_group.fl_electrode_group_creator import FlElectrodeGroupCreator
from fl.datamigration.nwb.components.electrode_group.fl_fl_electrode_group import FlFLElectrodeGroup
from fl.datamigration.tools.validate_input_parameters import validate_input_parameters


class FlElectrodeGroupManager:

    def __init__(self, electrode_groups_metadata):
        self.electrode_groups_metadata = electrode_groups_metadata

    def get_fl_fl_electrode_groups(self, probes):
        validate_input_parameters(__name__, self.electrode_groups_metadata, probes)

        return [FlFLElectrodeGroup(
            metadata=electrode_group_metadata,
            device=probes[counter]
        ) for counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata)]
