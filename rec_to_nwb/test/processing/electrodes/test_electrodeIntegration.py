import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dateutil.tz import tzlocal
from hdmf.common import DynamicTable
from pynwb import NWBFile
from pynwb.ecephys import ElectrodeGroup
from testfixtures import should_raise

from rec_to_nwb.processing.nwb.components.electrodes.electrode_creator import ElectrodesCreator
from rec_to_nwb.processing.nwb.components.electrodes.fl_electrode_manager import FlElectrodeManager

path = os.path.dirname(os.path.abspath(__file__))


class TestElectrodeIntegration(TestCase):

    def test_electrode_create_and_inject_inside_nwb_successfully(self):
        electrode_groups_metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}
        ]

        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 1, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 2, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 3, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0}]}]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                     {'id': 1, 'rel_x': 40.0, 'rel_y': 0.0, 'rel_z': 0.0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0.0, 'rel_y': 300.0, 'rel_z': 0.0},
                     {'id': 33, 'rel_x': 40.0, 'rel_y': 300.0, 'rel_z': 0.0}]},
                 {'shank_id': 2, 'electrodes': [
                     {'id': 64, 'rel_x': 0.0, 'rel_y': 600.0, 'rel_z': 0.0},
                     {'id': 65, 'rel_x': 40.0, 'rel_y': 600.0, 'rel_z': 0.0}, ]},
                 {'shank_id': 3, 'electrodes': [
                     {'id': 96, 'rel_x': 0.0, 'rel_y': 900.0, 'rel_z': 0.0},
                     {'id': 97, 'rel_x': 40.0, 'rel_y': 900.0, 'rel_z': 0.0}]}]}
        ]

        mock_electrodes_valid_map = [
            False, False, False, False,
            True, True, False, False,
            True, True, True, True
        ]
        mock_electrode_groups_valid_map = {1}

        mock_eg_1 = Mock(spec=ElectrodeGroup)
        mock_eg_2 = Mock(spec=ElectrodeGroup)
        mock_eg_1.name = '0'
        mock_eg_2.name = '1'

        nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        electrode_creator = ElectrodesCreator()
        fl_electrodes_manager = FlElectrodeManager(probes_metadata, electrode_groups_metadata)
        fl_electrodes = fl_electrodes_manager.get_fl_electrodes(
            electrode_groups=[mock_eg_2],
            electrodes_valid_map=mock_electrodes_valid_map,
            electrode_groups_valid_map=mock_electrode_groups_valid_map
        )
        [electrode_creator.create(nwb_file, fl_electrode) for fl_electrode in fl_electrodes]

        self.assertEqual(6, len(fl_electrodes))
        self.assertIsInstance(nwb_file.electrodes, DynamicTable)

        # id
        self.assertEqual(nwb_file.electrodes[0, 0], 4)
        self.assertEqual(nwb_file.electrodes[1, 0], 5)

        # x
        self.assertEqual(nwb_file.electrodes[0, 1], 0.0)
        self.assertEqual(nwb_file.electrodes[1, 1], 0.0)

        # y
        self.assertEqual(nwb_file.electrodes[0, 2], 0.0)
        self.assertEqual(nwb_file.electrodes[1, 2], 0.0)

        # z
        self.assertEqual(nwb_file.electrodes[0, 3], 0.0)
        self.assertEqual(nwb_file.electrodes[1, 3], 0.0)

        # imp
        self.assertEqual(nwb_file.electrodes[0, 4], 0.0)
        self.assertEqual(nwb_file.electrodes[1, 4], 0.0)

        # location
        self.assertEqual(nwb_file.electrodes[0, 5], 'None')
        self.assertEqual(nwb_file.electrodes[1, 5], 'None')

        # filtering
        self.assertEqual(nwb_file.electrodes[0, 6], 'None')
        self.assertEqual(nwb_file.electrodes[1, 6], 'None')

        # group
        self.assertEqual(nwb_file.electrodes[0, 7], mock_eg_2)
        self.assertEqual(nwb_file.electrodes[1, 7], mock_eg_2)

        # electrode_group name
        self.assertEqual(nwb_file.electrodes[0, 8], '1')
        self.assertEqual(nwb_file.electrodes[1, 8], '1')

    @should_raise(TypeError)
    def test_electrode_failed_creating_and_injecting_inside_nwb_due_to_None_NWB(self):
        electrode_groups_metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}
        ]

        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 1, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      ]}]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                     {'id': 1, 'rel_x': 40.0, 'rel_y': 0.0, 'rel_z': 0.0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0.0, 'rel_y': 300.0, 'rel_z': 0.0},
                     {'id': 33, 'rel_x': 40.0, 'rel_y': 300.0, 'rel_z': 0.0}]},
                 ]}
        ]
        mock_electrode_groups_valid_map = {0, 1}
        mock_eg_1 = Mock(spec=ElectrodeGroup)
        mock_eg_2 = Mock(spec=ElectrodeGroup)
        mock_eg_1.name = '0'
        mock_eg_2.name = '1'

        electrode_creator = ElectrodesCreator()

        fl_electrodes_manager = FlElectrodeManager(probes_metadata, electrode_groups_metadata)

        fl_electrodes = fl_electrodes_manager.get_fl_electrodes(
            electrode_groups=[mock_eg_1, mock_eg_2],
            electrodes_valid_map=[
                True, True, False, False, False, True
            ],
            electrode_groups_valid_map=mock_electrode_groups_valid_map
        )

        [electrode_creator.create(None, fl_electrode) for fl_electrode in fl_electrodes]
