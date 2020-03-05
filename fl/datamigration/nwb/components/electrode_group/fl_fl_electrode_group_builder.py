from fl.datamigration.nwb.components.electrode_group.fl_fl_electrode_group import FlFLElectrodeGroup


class FlFlElectrodeGroupBuilder:

    def build(self, metadata, device):
        return FlFLElectrodeGroup(metadata, device)