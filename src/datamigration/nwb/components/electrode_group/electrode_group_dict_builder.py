from src.datamigration.nwb.components.electrode_group.electrode_group_creator import ElectrodeGroupCreator


class ElectrodeGroupDictBuilder:

    def __init__(self, electrode_groups_metadata):
        self.electrode_groups_metadata = electrode_groups_metadata

        self.electrodes_group_creator = ElectrodeGroupCreator()

    def build(self, probes):
        electrode_groups = {}
        for counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata):
            electrode_groups[counter] = self.electrodes_group_creator.create_electrode_group(
                metadata=electrode_group_metadata,
                device=probes[counter]
            )
        return electrode_groups
