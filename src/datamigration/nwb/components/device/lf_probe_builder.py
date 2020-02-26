from src.datamigration.nwb.components.device.lf_probe import LfProbe


class LfProbeBuilder:

    def build(self, metadata, probe_id):
        return LfProbe(metadata, probe_id)