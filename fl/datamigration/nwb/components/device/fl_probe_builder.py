from fl.datamigration.nwb.components.device.fl_probe import FlProbe


class FlProbeBuilder:

    @staticmethod
    def build(metadata, electrode_group_id):
        return FlProbe(metadata, electrode_group_id)
