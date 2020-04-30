from fl.datamigration.nwb.components.device.fl_probe_builder import FlProbeBuilder
from fl.datamigration.tools.beartype.beartype import beartype
from fl.datamigration.tools.filter_probe_by_type import filter_probe_by_type
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlProbeManager:

    @beartype
    def __init__(self, probes_metadata: list, electrode_groups_metadata: list):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.fl_probe_builder = FlProbeBuilder()
        self.probe_id = -1

    @beartype
    def get_fl_probes(self, shanks_dict: dict, probes_valid_map_dict: dict):
        fl_probes = []
        probes_types = []
        for electrode_group_metadata in self.electrode_groups_metadata:
            device_type = electrode_group_metadata['device_type']

            if device_type not in probes_types:
                probes_types.append(device_type)
                if probes_valid_map_dict[device_type]:
                    probe_metadata = filter_probe_by_type(self.probes_metadata, device_type)

                    fl_probes.append(self._build_single_probe(
                        probe_metadata=probe_metadata,
                        shanks=shanks_dict[device_type])
                    )
        return fl_probes

    @beartype
    def _build_single_probe(self, probe_metadata: dict, shanks: list):
        self.probe_id += 1
        return self.fl_probe_builder.build(probe_metadata, self.probe_id, shanks)

