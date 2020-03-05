from fl.datamigration.nwb.components.electrode_group.fl_fl_electrode_group import LfFLElectrodeGroup


class LfFlElectrodeGroupBuilder:

    def build(self, metadata, device):
        return LfFLElectrodeGroup(metadata, device)