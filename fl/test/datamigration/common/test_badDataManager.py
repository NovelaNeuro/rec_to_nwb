from unittest import TestCase

from testfixtures import should_raise

from fl.datamigration.exceptions.bad_channels_exception import BadChannelsException
from fl.datamigration.metadata.bad_data_manager import BadDataManager


class TestBadDataManager(TestCase):

    def test_bad_data_manager_get_valid_map_dict_successfully(self):
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

        bad_data_manager = BadDataManager(
            metadata=metadata
        )
        electrodes_valid_map_dict = bad_data_manager.get_valid_map_dict()

        self.assertIsInstance(electrodes_valid_map_dict, dict)

        self.assertEqual(electrodes_valid_map_dict['electrodes'], [
            False, True, False, True, True, True, True, True, True, False, False, False, True, True, True, True
        ])
        self.assertEqual(electrodes_valid_map_dict['electrode_group'], [True, False, True, False])
        self.assertEqual(electrodes_valid_map_dict['probes'], [True, True, False])

    @should_raise(BadChannelsException)
    def test_bad_data_manager_get_valid_map_dict_end_nbw_building_process_due_to_lack_of_good_data(self):
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

        bad_data_manager = BadDataManager(
            metadata=metadata
        )
        bad_data_manager.get_valid_map_dict()
