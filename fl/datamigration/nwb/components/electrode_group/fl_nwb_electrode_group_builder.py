from fl.datamigration.nwb.components.electrode_group.fl_nwb_electrode_group import FlNwbElectrodeGroup


class FlNwbElectrodeGroupBuilder:

    def build(self, metadata, device):
        return FlNwbElectrodeGroup(metadata, device)