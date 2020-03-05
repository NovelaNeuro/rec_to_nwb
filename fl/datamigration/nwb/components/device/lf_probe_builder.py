from fl.datamigration.nwb.components.device.fl_probe import LfProbe


class LfProbeBuilder:

    @staticmethod
    def build(metadata, probe_id):
        return LfProbe(metadata, probe_id)