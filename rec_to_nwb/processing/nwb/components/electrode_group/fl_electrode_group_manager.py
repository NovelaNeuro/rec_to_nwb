from ndx_fl_novela.probe import Probe

from rec_to_nwb.processing.nwb.components.electrode_group.fl_electrode_group_builder import FlElectrodeGroupBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlElectrodeGroupManager:

    @beartype
    def __init__(self, electrode_groups_metadata: list):
        self.electrode_groups_metadata = electrode_groups_metadata

    @beartype
    def get_fl_electrode_groups(self, probes: list, electrode_groups_valid_map: set):
        fl_electrode_groups = []
        for electrode_group_metadata in self.electrode_groups_metadata:
            if electrode_group_metadata['id'] in electrode_groups_valid_map:
                probe = self.__get_probe_by_type(probes, electrode_group_metadata['device_type'])
                fl_electrode_groups.append(
                    FlElectrodeGroupBuilder.build(
                        metadata=electrode_group_metadata,
                        device=probe
                    )
                )
        return fl_electrode_groups

    @staticmethod
    @beartype
    def __get_probe_by_type(probes: list, probe_type: str) -> Probe:
        for probe in probes:
            if probe_type == probe.probe_type:
                return probe
