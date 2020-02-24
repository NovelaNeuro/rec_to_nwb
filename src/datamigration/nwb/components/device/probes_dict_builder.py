from src.datamigration.nwb.components.device.device_factory import DeviceFactory
from src.datamigration.nwb.components.device.probe_extractor import ProbesExtractor
from src.datamigration.utils.filter_probe_by_type import filter_probe_by_type


class ProbesDictBuilder:

    def __init__(self, probes_metadata, electrode_groups_metadata):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.probe_extractor = ProbesExtractor()
        self.device_factory = DeviceFactory()

    def build(self):
        probes = {}
        for probe_counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata):
            probes[probe_counter] = self._build_single_probe(electrode_group_metadata, probe_counter)
        return probes

    def _build_single_probe(self, electrode_group_metadata, probe_counter):
        probe_metadata = filter_probe_by_type(
            self.probes_metadata,
            electrode_group_metadata['device_type']
        )
        return self.device_factory.create_probe(probe_metadata, probe_counter)
