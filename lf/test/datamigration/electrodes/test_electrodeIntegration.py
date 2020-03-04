import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dateutil.tz import tzlocal
from hdmf.common import DynamicTable, VectorData, ElementIdentifiers
from pynwb import NWBFile

from ndx_lflab_novela.fl_electrode_group import FLElectrodeGroup
from testfixtures import should_raise

from lf.datamigration.exceptions.none_param_in_init_exception import NoneParamInInitException
from lf.datamigration.nwb.components.electrodes.electrode_creator import ElectrodesCreator
from lf.datamigration.nwb.components.electrodes.lf_electrode_manager import LfElectrodeManager

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
                      {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                     {'id': 1, 'rel_x': 40, 'rel_y': 0, 'rel_z': 0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0, 'rel_y': 300, 'rel_z': 0},
                     {'id': 33, 'rel_x': 40, 'rel_y': 300, 'rel_z': 0}]},
                 {'shank_id': 2, 'electrodes': [
                     {'id': 64, 'rel_x': 0, 'rel_y': 600, 'rel_z': 0},
                     {'id': 65, 'rel_x': 40, 'rel_y': 600, 'rel_z': 0}, ]},
                 {'shank_id': 3, 'electrodes': [
                     {'id': 96, 'rel_x': 0, 'rel_y': 900, 'rel_z': 0},
                     {'id': 97, 'rel_x': 40, 'rel_y': 900, 'rel_z': 0}]}]}
        ]
        
        mock_eg_1 = Mock()
        mock_eg_2 = Mock()
        mock_eg_1.__class__ = FLElectrodeGroup
        mock_eg_2.__class__ = FLElectrodeGroup
        mock_eg_1.name = 'FLElectrodeGroup1'
        mock_eg_2.name = 'FLElectrodeGroup2'

        nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )
        
        electrode_creator = ElectrodesCreator()

        lf_electrodes_manager = LfElectrodeManager(probes_metadata, electrode_groups_metadata)

        lf_electrodes = lf_electrodes_manager.get_lf_electrodes(
            electrode_groups=[mock_eg_1, mock_eg_2],
        )

        [electrode_creator.create(nwb_file, lf_electrode) for lf_electrode in lf_electrodes]

        self.assertEqual(12, len(lf_electrodes))
        self.assertIsInstance(nwb_file.electrodes, DynamicTable)

        self.assertEqual(nwb_file.electrodes[0][0], 0)
        self.assertEqual(nwb_file.electrodes[1][0], 1)

        self.assertEqual(nwb_file.electrodes[0][1], 0.0)
        self.assertEqual(nwb_file.electrodes[1][1], 0.0)

        self.assertEqual(nwb_file.electrodes[0][2], 0.0)
        self.assertEqual(nwb_file.electrodes[1][2], 0.0)

        self.assertEqual(nwb_file.electrodes[0][3], 0.0)
        self.assertEqual(nwb_file.electrodes[1][3], 0.0)

        self.assertEqual(nwb_file.electrodes[0][4], 0.0)
        self.assertEqual(nwb_file.electrodes[1][4], 0.0)

        self.assertEqual(nwb_file.electrodes[0][5], 'None')
        self.assertEqual(nwb_file.electrodes[1][5], 'None')

        self.assertEqual(nwb_file.electrodes[0][6], 'None')
        self.assertEqual(nwb_file.electrodes[1][6], 'None')

        self.assertEqual(nwb_file.electrodes[0][7], mock_eg_1)
        self.assertEqual(nwb_file.electrodes[1][7], mock_eg_1)

        self.assertEqual(nwb_file.electrodes[0][8], 'FLElectrodeGroup1')
        self.assertEqual(nwb_file.electrodes[1][8], 'FLElectrodeGroup1')

    @should_raise(NoneParamInInitException)
    def test_electrode_failed_creating_and_injecting_inside_nwb_due_to_None_param(self):
        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                     {'id': 1, 'rel_x': 40, 'rel_y': 0, 'rel_z': 0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0, 'rel_y': 300, 'rel_z': 0},
                     {'id': 33, 'rel_x': 40, 'rel_y': 300, 'rel_z': 0}]},
                 {'shank_id': 2, 'electrodes': [
                     {'id': 64, 'rel_x': 0, 'rel_y': 600, 'rel_z': 0},
                     {'id': 65, 'rel_x': 40, 'rel_y': 600, 'rel_z': 0}, ]},
                 {'shank_id': 3, 'electrodes': [
                     {'id': 96, 'rel_x': 0, 'rel_y': 900, 'rel_z': 0},
                     {'id': 97, 'rel_x': 40, 'rel_y': 900, 'rel_z': 0}]}]}
        ]

        mock_eg_1 = Mock()
        mock_eg_2 = Mock()
        mock_eg_1.__class__ = FLElectrodeGroup
        mock_eg_2.__class__ = FLElectrodeGroup
        mock_eg_1.name = 'FLElectrodeGroup1'
        mock_eg_2.name = 'FLElectrodeGroup2'

        nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        electrode_creator = ElectrodesCreator()

        lf_electrodes_manager = LfElectrodeManager(probes_metadata, None)

        lf_electrodes = lf_electrodes_manager.get_lf_electrodes(
            electrode_groups=[mock_eg_1, mock_eg_2],
        )

        [electrode_creator.create(nwb_file, lf_electrode) for lf_electrode in lf_electrodes]

    @should_raise(NoneParamInInitException)
    def test_electrode_failed_creating_and_injecting_inside_nwb_due_to_None_ElectrodeGroup(self):
        electrode_groups_metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}
        ]

        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                     {'id': 1, 'rel_x': 40, 'rel_y': 0, 'rel_z': 0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0, 'rel_y': 300, 'rel_z': 0},
                     {'id': 33, 'rel_x': 40, 'rel_y': 300, 'rel_z': 0}]},
                 {'shank_id': 2, 'electrodes': [
                     {'id': 64, 'rel_x': 0, 'rel_y': 600, 'rel_z': 0},
                     {'id': 65, 'rel_x': 40, 'rel_y': 600, 'rel_z': 0}, ]},
                 {'shank_id': 3, 'electrodes': [
                     {'id': 96, 'rel_x': 0, 'rel_y': 900, 'rel_z': 0},
                     {'id': 97, 'rel_x': 40, 'rel_y': 900, 'rel_z': 0}]}]}
        ]

        nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        electrode_creator = ElectrodesCreator()

        lf_electrodes_manager = LfElectrodeManager(probes_metadata, electrode_groups_metadata)

        lf_electrodes = lf_electrodes_manager.get_lf_electrodes(
            electrode_groups=None
        )

        [electrode_creator.create(nwb_file, lf_electrode) for lf_electrode in lf_electrodes]

    @should_raise(NoneParamInInitException)
    def test_electrode_failed_creating_and_injecting_inside_nwb_due_to_None_ElectrodeGroup_attr(self):
        electrode_groups_metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}
        ]

        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                     {'id': 1, 'rel_x': 40, 'rel_y': 0, 'rel_z': 0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0, 'rel_y': 300, 'rel_z': 0},
                     {'id': 33, 'rel_x': 40, 'rel_y': 300, 'rel_z': 0}]},
                 {'shank_id': 2, 'electrodes': [
                     {'id': 64, 'rel_x': 0, 'rel_y': 600, 'rel_z': 0},
                     {'id': 65, 'rel_x': 40, 'rel_y': 600, 'rel_z': 0}, ]},
                 {'shank_id': 3, 'electrodes': [
                     {'id': 96, 'rel_x': 0, 'rel_y': 900, 'rel_z': 0},
                     {'id': 97, 'rel_x': 40, 'rel_y': 900, 'rel_z': 0}]}]}
        ]

        mock_eg_1 = Mock()
        mock_eg_2 = Mock()
        mock_eg_1.__class__ = FLElectrodeGroup
        mock_eg_2.__class__ = FLElectrodeGroup
        mock_eg_1.name = None
        mock_eg_2.name = None

        nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        electrode_creator = ElectrodesCreator()

        lf_electrodes_manager = LfElectrodeManager(probes_metadata, electrode_groups_metadata)

        lf_electrodes = lf_electrodes_manager.get_lf_electrodes(
            electrode_groups=[mock_eg_1, mock_eg_2]
        )

        [electrode_creator.create(nwb_file, lf_electrode) for lf_electrode in lf_electrodes]

    @should_raise(NoneParamInInitException)
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
                      {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                     {'id': 1, 'rel_x': 40, 'rel_y': 0, 'rel_z': 0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0, 'rel_y': 300, 'rel_z': 0},
                     {'id': 33, 'rel_x': 40, 'rel_y': 300, 'rel_z': 0}]},
                 {'shank_id': 2, 'electrodes': [
                     {'id': 64, 'rel_x': 0, 'rel_y': 600, 'rel_z': 0},
                     {'id': 65, 'rel_x': 40, 'rel_y': 600, 'rel_z': 0}, ]},
                 {'shank_id': 3, 'electrodes': [
                     {'id': 96, 'rel_x': 0, 'rel_y': 900, 'rel_z': 0},
                     {'id': 97, 'rel_x': 40, 'rel_y': 900, 'rel_z': 0}]}]}
        ]

        mock_eg_1 = Mock()
        mock_eg_2 = Mock()
        mock_eg_1.__class__ = FLElectrodeGroup
        mock_eg_2.__class__ = FLElectrodeGroup
        mock_eg_1.name = 'FLElectrodeGroup1'
        mock_eg_2.name = 'FLElectrodeGroup2'

        electrode_creator = ElectrodesCreator()

        lf_electrodes_manager = LfElectrodeManager(probes_metadata, electrode_groups_metadata)

        lf_electrodes = lf_electrodes_manager.get_lf_electrodes(
            electrode_groups=[mock_eg_1, mock_eg_2],
        )

        [electrode_creator.create(None, lf_electrode) for lf_electrode in lf_electrodes]
