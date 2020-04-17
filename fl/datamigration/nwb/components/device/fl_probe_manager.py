from fl.datamigration.nwb.components.device.fl_probe_builder import FlProbeBuilder
from fl.datamigration.tools.filter_probe_by_type import filter_probe_by_type
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlProbeManager:

    def __init__(self, probes_metadata, electrode_groups_metadata):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.fl_probe_builder = FlProbeBuilder()
        self.probe_id = -1

    def get_fl_probes_list(self):
        validate_parameters_not_none(__name__, self.probes_metadata, self.electrode_groups_metadata)
        fl_probes = []
        probes_types = []
        for electrode_group_metadata in self.electrode_groups_metadata:
            if electrode_group_metadata['device_type'] not in probes_types:
                probes_types.append(electrode_group_metadata['device_type'])
                probe_metadata = filter_probe_by_type(self.probes_metadata, electrode_group_metadata['device_type'])

                fl_probes.append(self._build_single_probe(probe_metadata, shanks))
        return fl_probes



    def _build_single_probe(self, probe_metadata, shanks):
        self.probe_id += 1
        return self.fl_probe_builder.build(probe_metadata, self.probe_id, shanks)

