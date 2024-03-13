from ndx_franklab_novela import Probe
from rec_to_nwb.processing.nwb.components.electrode_group.fl_nwb_electrode_group_builder import \
    FlNwbElectrodeGroupBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlNwbElectrodeGroupManager:
    """Manage ElectrodeGroup data and call FlNwbElectrodeGroupBuilder to create list of FlNwbElectrodeGroupBuilder.

    Args:
        electrode_groups_metadata (list): list that contains electrode group metadata dicts

    Methods:
        get_fl_nwb_electrode_groups()
    """
    @beartype
    def __init__(self, electrode_groups_metadata: list):
        self.electrode_groups_metadata = electrode_groups_metadata

    @beartype
    def get_fl_nwb_electrode_groups(self, probes: list, electrode_groups_valid_map: set):
        """Manage ElectrodeGroup data and call FlNwbElectrodeGroupBuilder to create list of FlNwbElectrodeGroupBuilder.

        Args:
            probes (list): list of existing probes
            electrode_groups_valid_map (set): Set of electrode groups ids that are not corrupted

        Returns:
            list: list with FlNwbElectrodeGroupBuilder objects
        """

        fl_nwb_electrode_groups = []
        for electrode_group_metadata in self.electrode_groups_metadata:
            if electrode_group_metadata['id'] in electrode_groups_valid_map:
                probe = self.__get_probe_by_type(
                    probes, electrode_group_metadata['device_type'])
                fl_nwb_electrode_groups.append(
                    FlNwbElectrodeGroupBuilder.build(
                        metadata=electrode_group_metadata,
                        device=probe
                    )
                )
        return fl_nwb_electrode_groups

    @staticmethod
    @beartype
    def __get_probe_by_type(probes: list, probe_type: str) -> Probe:
        for probe in probes:
            if probe_type == probe.probe_type:
                return probe
