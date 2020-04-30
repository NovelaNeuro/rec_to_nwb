import copy

from ndx_fl_novela.probe import Probe

from fl.datamigration.nwb.components.electrode_group.fl_electrode_group import FlElectrodeGroup
from fl.datamigration.tools.beartype.beartype import beartype


class FlElectrodeGroupManager:

    @beartype
    def __init__(self, electrode_groups_metadata: list):
        self.electrode_groups_metadata = electrode_groups_metadata

    @beartype
    def get_fl_electrode_groups(self, probes: list, electrode_groups_valid_map: list):
        tmp_electrode_groups_valid_map = copy.deepcopy(electrode_groups_valid_map)

        fl_electrode_groups = []
        for electrode_group_metadata in self.electrode_groups_metadata:
            if tmp_electrode_groups_valid_map.pop(0):
                probe = self.__get_probe_by_type(probes, electrode_group_metadata['device_type'])
                fl_electrode_groups.append(
                    FlElectrodeGroup(
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
