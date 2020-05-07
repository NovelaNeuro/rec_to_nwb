import copy

from pynwb.ecephys import ElectrodeGroup

from rec_to_nwb.processing.nwb.components.electrodes.fl_electrode_builder import FlElectrodesBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.filter_probe_by_type import filter_probe_by_type
from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_not_none


class FlElectrodeManager:

    @beartype
    def __init__(self, probes_metadata: list, electrode_groups_metadata: list):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.fl_electrodes_builder = FlElectrodesBuilder()

    @beartype
    def get_fl_electrodes(self, electrode_groups: list, electrodes_valid_map: list, electrode_groups_valid_map: set):
        self.__validate_parameters(electrode_groups)
        tmp_electrodes_valid_map = copy.deepcopy(electrodes_valid_map)

        fl_electrodes = []
        fl_electrode_id = -1
        for electrode_group_metadata in self.electrode_groups_metadata:
            probe_metadata = filter_probe_by_type(self.probes_metadata, electrode_group_metadata['device_type'])

            for shank in probe_metadata['shanks']:
                for _ in shank['electrodes']:
                    fl_electrode_id += 1

                    if tmp_electrodes_valid_map.pop(0) and \
                            (electrode_group_metadata['id'] in electrode_groups_valid_map):

                        fl_electrodes.append(
                            self.fl_electrodes_builder.build(
                                fl_electrode_id,
                                self.__get_electrode_group(electrode_group_metadata, electrode_groups)
                            )
                        )
        return fl_electrodes

    @staticmethod
    def __get_electrode_group(electrode_group_metadata, electrode_groups):
        return [electrode_group
                for electrode_group in electrode_groups
                if electrode_group.name == 'electrode group ' + str(electrode_group_metadata['id'])
                ][0]

    @staticmethod
    @beartype
    def __validate_parameters(electrode_groups: list):
        [validate_parameters_not_none(__name__, electrode_group.name) for electrode_group in electrode_groups]
