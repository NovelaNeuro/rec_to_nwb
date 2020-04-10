from fl.datamigration.nwb.components.device.fl_probe_builder import FlProbeBuilder
from fl.datamigration.tools.filter_probe_by_type import filter_probe_by_type
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlProbeManager:

    def __init__(self, probes_metadata, electrode_groups_metadata):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.fl_probe_builder = FlProbeBuilder()

    def get_fl_probes_list(self):
        validate_parameters_not_none(__name__, self.probes_metadata, self.electrode_groups_metadata)
        return [self._build_single_probe(electrode_group_metadata, probe_counter)
                for probe_counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata)]

    def _build_single_probe(self, electrode_group_metadata, probe_counter):
        probe_metadata = filter_probe_by_type(
            self.probes_metadata,
            electrode_group_metadata['device_type']
        )
        return self.fl_probe_builder.build(probe_metadata, probe_counter)
