from fl.datamigration.nwb.components.device.fl_probe import FlProbe


class FlProbeBuilder:

    @staticmethod
    def build(metadata, probe_id):
        return FlProbe(metadata, probe_id)
