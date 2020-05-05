from fl.datamigration.nwb.components.device.fl_probe_builder import FlProbeBuilder
from fl.datamigration.tools.beartype.beartype import beartype
from fl.datamigration.tools.filter_probe_by_type import filter_probe_by_type


class FlProbeManager:

    @beartype
    def __init__(self, probes_metadata: list):
        self.probes_metadata = probes_metadata

        self.fl_probe_builder = FlProbeBuilder()
        self.probe_id = -1

    @beartype
    def get_fl_probes(self, shanks_dict: dict, probes_valid_map: set):
        fl_probes = []
        for probe_type in probes_valid_map:
            probe_metadata = filter_probe_by_type(self.probes_metadata, probe_type)

            fl_probes.append(self._build_single_probe(
                probe_metadata=probe_metadata,
                shanks=shanks_dict[probe_type])
            )
        return fl_probes

    @beartype
    def _build_single_probe(self, probe_metadata: dict, shanks: list):
        self.probe_id += 1
        return self.fl_probe_builder.build(probe_metadata, self.probe_id, shanks)

