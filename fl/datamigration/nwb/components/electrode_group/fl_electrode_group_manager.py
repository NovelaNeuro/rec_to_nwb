from fl.datamigration.nwb.components.electrode_group.electrode_group_factory import ElectrodeGroupFactory
from fl.datamigration.nwb.components.electrode_group.fl_nwb_electrode_group import FlNwbElectrodeGroup
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlElectrodeGroupManager:

    def __init__(self, electrode_groups_metadata):
        self.electrode_groups_metadata = electrode_groups_metadata

    def get_fl_nwb_electrode_groups(self, probes):
        validate_parameters_not_none(__name__, self.electrode_groups_metadata, probes)

        fl_nwb_electrode_groups = []
        for electrode_group_metadata in self.electrode_groups_metadata:
            probe = self.__get_probe_by_type(probes, electrode_group_metadata['device_type'])
            fl_nwb_electrode_groups.append(
                FlNwbElectrodeGroup(
                    metadata=electrode_group_metadata,
                    device=probe
                )
            )
        return fl_nwb_electrode_groups

    @staticmethod
    def __get_probe_by_type(probes, probe_type):
        for probe in probes:
            if probe_type == probe.probe_type:
                return probe
