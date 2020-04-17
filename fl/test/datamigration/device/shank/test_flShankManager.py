from unittest import TestCase
from unittest.mock import Mock

from ndx_fllab_novela.probe import ShanksElectrode
from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.device.shanks.fl_shank import FlShank
from fl.datamigration.nwb.components.device.shanks.fl_shank_manager import FlShankManager
from fl.datamigration.nwb.components.device.shanks_electrodes.fl_shanks_electrode import FlShanksElectrode


class TestFlShankManager(TestCase):

    def test_fl_shank_manager_create_fl_shanks_dict_successfully(self):
        electrode_groups_metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'},
            {'id': 3, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 3'}
        ]

        probes_metadata_1 = {
            'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1, 'shanks': [
                {
                    'shank_id': 0, 'electrodes': [
                    {'id': 0, 'rel_x': 11, 'rel_y': 22, 'rel_z': 33},
                    {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                    ]}]}
        probes_metadata_2 = {
            'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
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
               ]}

        mock_shanks_electrode_1 = Mock(spec=ShanksElectrode)
        mock_shanks_electrode_2 = Mock(spec=ShanksElectrode)
        mock_shanks_electrode_3 = Mock(spec=ShanksElectrode)
        mock_shanks_electrode_4 = Mock(spec=ShanksElectrode)
        mock_shanks_electrode_5 = Mock(spec=ShanksElectrode)
        mock_shanks_electrode_6 = Mock(spec=ShanksElectrode)
        mock_shanks_electrodes_dict = {
            'tetrode_12.5': [mock_shanks_electrode_1, mock_shanks_electrode_2],
            '128c-4s8mm6cm-20um-40um-sl': [mock_shanks_electrode_1, mock_shanks_electrode_2,
                                           mock_shanks_electrode_3, mock_shanks_electrode_4,
                                           mock_shanks_electrode_5, mock_shanks_electrode_6]
        }

        fl_shank_manager = FlShankManager(
            probes_metadata=[probes_metadata_1, probes_metadata_2],
            electrode_groups_metadata=electrode_groups_metadata
        )
        fl_shanks_dict = fl_shank_manager.get_fl_shanks_dict(mock_shanks_electrodes_dict)

        self.assertIsInstance(fl_shanks_dict, dict)
        self.assertIsInstance(fl_shanks_dict[probes_metadata_1['probe_type']], list)
        self.assertIsInstance(fl_shanks_dict[probes_metadata_1['probe_type']][0], FlShank)
        self.assertIsInstance(fl_shanks_dict[probes_metadata_1['probe_type']][0].shanks_electrodes, list)
        self.assertIsInstance(fl_shanks_dict[probes_metadata_1['probe_type']][0].shanks_electrodes[0], ShanksElectrode)

        self.assertEqual(len(fl_shanks_dict), 2)
        self.assertEqual(len(fl_shanks_dict[probes_metadata_1['probe_type']]), 1)
        self.assertEqual(len(fl_shanks_dict[probes_metadata_2['probe_type']]), 3)
    
        self.assertEqual(fl_shanks_dict[probes_metadata_1['probe_type']][0].shank_id, 0)
        self.assertEqual(fl_shanks_dict[probes_metadata_1['probe_type']][0].shanks_electrodes,[
            mock_shanks_electrode_1, mock_shanks_electrode_2
        ])

        self.assertEqual(fl_shanks_dict[probes_metadata_2['probe_type']][0].shank_id, 0)
        self.assertEqual(fl_shanks_dict[probes_metadata_2['probe_type']][1].shank_id, 1)
        self.assertEqual(fl_shanks_dict[probes_metadata_2['probe_type']][0].shanks_electrodes, [
            mock_shanks_electrode_1, mock_shanks_electrode_2
        ])
        self.assertEqual(fl_shanks_dict[probes_metadata_2['probe_type']][1].shanks_electrodes, [
            mock_shanks_electrode_3, mock_shanks_electrode_4
        ])
        self.assertEqual(fl_shanks_dict[probes_metadata_2['probe_type']][2].shanks_electrodes, [
            mock_shanks_electrode_5, mock_shanks_electrode_6
        ])

    @should_raise(NoneParamException)
    def test_fl_shank_manager_failed_due_to_None_param(self):
        FlShankManager(
            probes_metadata=None,
            electrode_groups_metadata=None
        )

    @should_raise(NoneParamException)
    def test_fl_shank_manager_failed_creating_fl_shanks_dict_due_to_None_param(self):
        fl_shank_manager = FlShankManager(
            probes_metadata=Mock(spec=list),
            electrode_groups_metadata=Mock(spec=list)
        )
        fl_shank_manager.get_fl_shanks_dict(None)

