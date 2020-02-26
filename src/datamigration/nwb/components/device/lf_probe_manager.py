from src.datamigration.nwb.components.device.device_factory import DeviceFactory
from src.datamigration.nwb.components.device.lf_probe_builder import LfProbeBuilder
from src.datamigration.nwb.components.device.lf_probe_extractor import LfProbesExtractor
from src.datamigration.tools.filter_probe_by_type import filter_probe_by_type


class LfProbeManager:

    def __init__(self, probes_metadata, electrode_groups_metadata):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.lf_probe_extractor = LfProbesExtractor()
        self.lf_probe_builder = LfProbeBuilder()

    def get_lf_probes_list(self):
        return [self._build_single_probe(electrode_group_metadata, probe_counter)
                for probe_counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata)]

    def _build_single_probe(self, electrode_group_metadata, probe_counter):
        probe_metadata = filter_probe_by_type(
            self.probes_metadata,
            electrode_group_metadata['device_type']
        )
        return self.lf_probe_builder.build(probe_metadata, probe_counter)
