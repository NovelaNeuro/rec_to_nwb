import copy


from fl.datamigration.exceptions.bad_channels_exception import CorruptedDataException
from fl.datamigration.tools.beartype.beartype import beartype


class CorruptedDataManager:

    @beartype
    def __init__(self, metadata: dict):
        self.metadata = metadata

    @beartype
    def get_valid_map_dict(self) -> dict:

        electrodes_valid_map = self.__get_electrodes_valid_map(
            ntrode_metadata=self.metadata['ntrode electrode group channel map']
        )
        electrode_groups_valid_map = self.__get_electrode_groups_valid_map(
            electrode_groups_metadata=self.metadata['electrode groups'],
            ntrode_metadata=self.metadata['ntrode electrode group channel map'],
            electrodes_valid_map=electrodes_valid_map
        )
        probes_valid_map_dict = self.__get_probes_valid_map(
            electrode_groups_metadata=self.metadata['electrode groups'],
            electrode_groups_valid_map=electrode_groups_valid_map
        )

        self.__validate_data(probes_valid_map_dict)

        return {
            'electrodes': electrodes_valid_map,
            'electrode_group': electrode_groups_valid_map,
            'probes_dict': probes_valid_map_dict,
        }

    @staticmethod
    @beartype
    def __get_electrodes_valid_map(ntrode_metadata: list) -> list:
        electrodes_valid_map = []
        for ntrode in ntrode_metadata:
            electrodes_valid_map.extend(
                [bool(counter not in ntrode['bad_channels']) for counter, _ in enumerate(ntrode['map'])]
            )
        return electrodes_valid_map

    @staticmethod
    @beartype
    def __get_electrode_groups_valid_map(electrode_groups_metadata: list, ntrode_metadata: list,
                                         electrodes_valid_map: list) -> list:
        electrode_group_valid_map = [False for _ in electrode_groups_metadata]
        tmp_electrodes_valid_map = copy.deepcopy(electrodes_valid_map)

        for ntrode in ntrode_metadata:
            electrode_group_id = ntrode['electrode_group_id']
            for _ in ntrode['map']:
                if tmp_electrodes_valid_map.pop(0):
                    electrode_group_valid_map[electrode_group_id] = True
        return electrode_group_valid_map

    @staticmethod
    @beartype
    def __get_probes_valid_map(electrode_groups_metadata: list, electrode_groups_valid_map: list) -> dict:
        tmp_electrode_groups_valid_map = copy.deepcopy(electrode_groups_valid_map)

        probes_valid_map_dict = {}
        for electrode_group in electrode_groups_metadata:
            device_type = electrode_group['device_type']

            if tmp_electrode_groups_valid_map.pop(0):
                probes_valid_map_dict[device_type] = True
            elif not probes_valid_map_dict.get(device_type, False):
                probes_valid_map_dict[device_type] = False

        return probes_valid_map_dict

    @staticmethod
    @beartype
    def __validate_data(probes_valid_map_dict: dict):
        corrupted_data = True

        for probe_value in probes_valid_map_dict.values():
            if probe_value:
                corrupted_data = False
        if corrupted_data:
            raise CorruptedDataException('All data are corrupted')
