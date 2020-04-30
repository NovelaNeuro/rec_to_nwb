from fl.datamigration.nwb.components.electrode_group.fl_electrode_group import FlElectrodeGroup


class FlElectrodeGroupBuilder:

    @staticmethod
    def build(metadata, device):
        return FlElectrodeGroup(metadata, device)
