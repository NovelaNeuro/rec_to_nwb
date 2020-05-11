from unittest import TestCase
from unittest.mock import Mock

from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.corrupted_data_exception import CorruptedDataException
from rec_to_nwb.processing.metadata.corrupted_data_manager import CorruptedDataManager


class TestCorruptedDataManager(TestCase):

    def test_corrupted_data_manager_get_valid_map_dict_successfully(self):
        metadata = {
            'ntrode electrode group channel map': [
                {'ntrode_id': 1, 'electrode_group_id': 0, 'bad_channels': [1],
                 'map': {0: 0, 1: 1}},
                {'ntrode_id': 2, 'electrode_group_id': 0, 'bad_channels': [1],
                 'map': {0: 2, 1: 3}},
                {'ntrode_id': 3, 'electrode_group_id': 1, 'bad_channels': [0, 1],
                 'map': {0: 4, 1: 5}},
                {'ntrode_id': 4, 'electrode_group_id': 1, 'bad_channels': [0, 1],
                 'map': {0: 6, 1: 7}},
                {'ntrode_id': 5, 'electrode_group_id': 2, 'bad_channels': [0],
                 'map': {0: 8, 1: 9}},
                {'ntrode_id': 6, 'electrode_group_id': 2, 'bad_channels': [],
                 'map': {0: 10, 1: 11}},
                {'ntrode_id': 7, 'electrode_group_id': 3, 'bad_channels': [0, 1],
                 'map': {0: 12, 1: 13}},
                {'ntrode_id': 8, 'electrode_group_id': 3, 'bad_channels': [0, 1],
                 'map': {0: 14, 1: 15}}
            ],
            'electrode groups': [
                {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                 'description': 'Probe 1'},
                {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl',
                 'description': 'Probe 2'},
                {'id': 2, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl',
                 'description': 'Probe 3'},
                {'id': 3, 'location': 'mPFC', 'device_type': '32c-2s8mm6cm-20um-40um-dl',
                 'description': 'Probe 4'}
            ]
        }

        corrupted_data_manager = CorruptedDataManager(
            metadata=metadata
        )
        valid_map_dict = corrupted_data_manager.get_valid_map_dict()

        self.assertIsInstance(valid_map_dict, dict)

        self.assertEqual(valid_map_dict['electrodes'], [
            True, False,
            True, False,
            False, False,
            False, False,
            False, True,
            True, True,
            False, False,
            False, False
        ])
        self.assertEqual(valid_map_dict['electrode_groups'], {0, 2})
        self.assertEqual(valid_map_dict['probes'], {'128c-4s8mm6cm-20um-40um-sl','tetrode_12.5'})

    @should_raise(TypeError)
    def test_corrupted_data_manager_get_valid_map_dict_failed_due_to_none_param(self):
        CorruptedDataManager(
            metadata=None
        )

    @should_raise(TypeError)
    def test_corrupted_data_manager_get_valid_map_dict_failed_due_to_bad_type_param(self):
        metadata = [
            {'mock_key': 123}
        ]

        CorruptedDataManager(
            metadata=metadata
        )

    @should_raise(CorruptedDataException)
    def test_corrupted_data_manager_get_valid_map_dict_end_nbw_building_process_due_to_lack_of_good_data(self):
        metadata = {
            'ntrode electrode group channel map': [
                {'ntrode_id': 1, 'electrode_group_id': 0, 'bad_channels': [0, 1], 'map': {0: 0, 1: 1}},
                {'ntrode_id': 2, 'electrode_group_id': 1, 'bad_channels': [0, 1], 'map': {0: 2, 1: 3}},
            ],
            'electrode groups': [
                {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                 'description': 'Probe 1'},
                {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl',
                 'description': 'Probe 2'},
            ]
        }

        corrupted_data_manager = CorruptedDataManager(
            metadata=metadata
        )
        corrupted_data_manager.get_valid_map_dict()
