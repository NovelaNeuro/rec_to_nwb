from rec_to_nwb.processing.exceptions.corrupted_data_exception import \
    CorruptedDataException
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class CorruptedDataManager:
    """Manager collect only correct data. Raise exception if data are corrupted.

    Args:
        metadata (dict): parsed metadata
    """

    @beartype
    def __init__(self, metadata: dict):
        self.metadata = metadata

    @beartype
    def get_valid_map_dict(self) -> dict:
        """Get dictionary with correct data or raise exception

        Returns:
            dict: Dictionary with correct data.

        Raises:
            CorruptedDataException: If all data in metadata are corrupted
        """

        electrodes_valid_map = self.__get_electrodes_valid_map(
            ntrode_metadata=self.metadata['ntrode_electrode_group_channel_map']
        )
        electrode_groups_valid_map = self.__get_electrode_groups_valid_map(
            ntrode_metadata=self.metadata['ntrode_electrode_group_channel_map'],
            electrodes_valid_map=electrodes_valid_map
        )
        probes_valid_map = self.__get_probes_valid_map(
            electrode_groups_metadata=self.metadata['electrode_groups'],
            electrode_groups_valid_map=electrode_groups_valid_map
        )

        self.__validate_data(probes_valid_map)

        return {
            'electrodes': electrodes_valid_map,
            'electrode_groups': electrode_groups_valid_map,
            'probes': probes_valid_map,
        }

    @staticmethod
    @beartype
    def __get_electrodes_valid_map(ntrode_metadata: list) -> list:
        electrodes_valid_map = []
        for ntrode in ntrode_metadata:
            bad_channels = [int(bad_channel)
                            for bad_channel in ntrode['bad_channels']]
            electrodes_valid_map.extend(
                [bool(int(channel) not in bad_channels)
                 for channel in ntrode['map']]
            )
        return electrodes_valid_map

    @beartype
    def __get_electrode_groups_valid_map(self, ntrode_metadata: list,
                                         electrodes_valid_map: list) -> set:
        return {
            ntrode['electrode_group_id'] for ntrode in ntrode_metadata
        }

    @staticmethod
    @beartype
    def __get_probes_valid_map(electrode_groups_metadata: list, electrode_groups_valid_map: set) -> set:
        return {
            electrode_group['device_type']
            for electrode_group in electrode_groups_metadata
            if electrode_group['id'] in electrode_groups_valid_map
        }

    @staticmethod
    def __validate_data(probes_valid_map):
        corrupted_data = True

        for probe_type in probes_valid_map:
            if probe_type:
                corrupted_data = False
        if corrupted_data:
            raise CorruptedDataException(
                'There is no valid data to create probe')
