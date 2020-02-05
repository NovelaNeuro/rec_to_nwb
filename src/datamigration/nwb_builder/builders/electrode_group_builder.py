from src.datamigration.nwb_builder.creators.electrode_group_creator import ElectrodeGroupCreator


class ElectrodeGroupBuilder:

    def __init__(self):
        self.electrodes_group_creator = ElectrodeGroupCreator()

    def build(self, electrode_groups_metadata, probes):
        electrode_groups = {}
        for counter, electrode_group_metadata in enumerate(electrode_groups_metadata):
            electrode_groups[counter] = self.electrodes_group_creator.create_electrode_group(
                metadata=electrode_group_metadata,
                device=probes[counter]
            )
        return electrode_groups
