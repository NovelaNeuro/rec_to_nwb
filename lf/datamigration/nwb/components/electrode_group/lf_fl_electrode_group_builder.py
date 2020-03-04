from lf.datamigration.nwb.components.electrode_group.lf_fl_electrode_group import LfFLElectrodeGroup


class LfFlElectrodeGroupBuilder:

    def build(self, metadata, device):
        return LfFLElectrodeGroup(metadata, device)