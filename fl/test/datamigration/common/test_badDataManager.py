from unittest import TestCase

from testfixtures import should_raise

from fl.datamigration.exceptions.bad_channels_exception import BadChannelsException
from fl.datamigration.nwb.common.bad_data_manager import BadDataManager


class TestBadDataManager(TestCase):

    def test_bad_data_manager_return_electrodes_valid_map_successfully(self):
        metadata = {
            'ntrode electrode group channel map': [
                {'ntrode_id': 1, 'electrode_group_id': 0, 'bad_channels': [0, 2],
                 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
                {'ntrode_id': 2, 'electrode_group_id': 0, 'bad_channels': [0, 3],
                 'map': {0: 5, 1: 6, 2: 7, 3: 8, 4: 9}},
                {'ntrode_id': 3, 'electrode_group_id': 1, 'bad_channels': [0, 1],
                 'map': {0: 10, 1: 11, 2: 12, 3: 13, 4: 14}},
                {'ntrode_id': 4, 'electrode_group_id': 1, 'bad_channels': [0, 2, 3],
                 'map': {0: 15, 1: 16, 2: 17, 3: 18, 4: 19}}
            ]
        }

        bad_data_manager = BadDataManager(
            metadata=metadata
        )
        electrodes_valid_map = bad_data_manager.get_electrodes_valid_map()

        self.assertIsInstance(electrodes_valid_map, list)
        self.assertIsInstance(electrodes_valid_map[0], bool)

        self.assertEqual(electrodes_valid_map, [
            True, False, True, False, False, True, False, False, True, False, True, True, False, False, False, True,
            False, True, True, False
        ])

    def test_bad_data_manager_return_electrode_groups_valid_map_successfully(self):
        metadata = {
            'ntrode electrode group channel map': [
                {'ntrode_id': 1, 'electrode_group_id': 0, 'bad_channels': [0, 2],
                 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
                {'ntrode_id': 2, 'electrode_group_id': 0, 'bad_channels': [0, 3],
                 'map': {0: 5, 1: 6, 2: 7, 3: 8, 4: 9}},
                {'ntrode_id': 3, 'electrode_group_id': 1, 'bad_channels': [0, 1, 2, 3, 4],
                 'map': {0: 10, 1: 11, 2: 12, 3: 13, 4: 14}},
                {'ntrode_id': 4, 'electrode_group_id': 1, 'bad_channels': [0, 1, 2, 3, 4],
                 'map': {0: 15, 1: 16, 2: 17, 3: 18, 4: 19}}
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
        electrode_groups_valid_map = bad_data_manager.get_electrode_groups_valid_map()

        self.assertIsInstance(electrode_groups_valid_map, list)
        self.assertIsInstance(electrode_groups_valid_map[0], bool)

        self.assertEqual(electrode_groups_valid_map, [True, False])

    def test_bad_data_manager_return_probes_valid_map_successfully(self):
        metadata = {
            'ntrode electrode group channel map': [
                {'ntrode_id': 1, 'electrode_group_id': 0, 'bad_channels': [0, 2],
                 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
                {'ntrode_id': 2, 'electrode_group_id': 0, 'bad_channels': [0, 3],
                 'map': {0: 5, 1: 6, 2: 7, 3: 8, 4: 9}},
                {'ntrode_id': 3, 'electrode_group_id': 1, 'bad_channels': [0, 1, 2, 3, 4],
                 'map': {0: 10, 1: 11, 2: 12, 3: 13, 4: 14}},
                {'ntrode_id': 4, 'electrode_group_id': 1, 'bad_channels': [0, 1, 2, 3, 4],
                 'map': {0: 15, 1: 16, 2: 17, 3: 18, 4: 19}},
                {'ntrode_id': 5, 'electrode_group_id': 2, 'bad_channels': [0, 1],
                 'map': {0: 20, 1: 21, 2: 22, 3: 23, 4: 24}},
                {'ntrode_id': 6, 'electrode_group_id': 2, 'bad_channels': [0, 4],
                 'map': {0: 25, 1: 26, 2: 27, 3: 28, 4: 29}}
                {'ntrode_id': 7, 'electrode_group_id': 3, 'bad_channels': [0, 1, 2, 3, 4],
                 'map': {0: 30, 1: 31, 2: 32, 3: 33, 4: 34}},
                {'ntrode_id': 8, 'electrode_group_id': 3, 'bad_channels': [0, 1, 2, 3, 4],
                 'map': {0: 35, 1: 36, 2: 37, 3: 38, 4: 39}}
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
        electrode_groups_valid_map = bad_data_manager.get_probes_valid_map()

        self.assertIsInstance(electrode_groups_valid_map, list)
        self.assertIsInstance(electrode_groups_valid_map[0], bool)

        self.assertEqual(electrode_groups_valid_map, [True, True, False])

    @should_raise(BadChannelsException)
    def test_bad_data_manager_in_electrodes_valid_map_end_nbw_building_process_due_to_lack_of_good_data(self):
        metadata = {
            'ntrode electrode group channel map': [
                {'ntrode_id': 1, 'electrode_group_id': 0, 'bad_channels': [0, 1], 'map': {0: 0, 1: 1}},
                {'ntrode_id': 2, 'electrode_group_id': 0, 'bad_channels': [0, 1], 'map': {0: 2, 1: 3}},
            ]
        }

        bad_data_manager = BadDataManager(
            metadata=metadata
        )
        bad_data_manager.get_electrodes_valid_map()

    @should_raise(BadChannelsException)
    def test_bad_data_manager_in_electrode_groups_valid_map_end_nbw_building_process_due_to_lack_of_good_data(self):
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
        bad_data_manager.get_electrode_groups_valid_map()

    @should_raise(BadChannelsException)
    def test_bad_data_manager_in_probes_valid_map_end_nbw_building_process_due_to_lack_of_good_data(self):
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
        bad_data_manager.get_probes_valid_map()