from unittest import TestCase

from testfixtures import should_raise

from rec_to_nwb.processing.nwb.components.device.shanks_electrodes.fl_shanks_electrode import FlShanksElectrode
from rec_to_nwb.processing.nwb.components.device.shanks_electrodes.fl_shanks_electrode_manager import \
    FlShanksElectrodeManager


class TestFlShanksElectrodeManager(TestCase):

    def test_fl_shanks_electrode_manager_create_fl_shanks_electrodes_dict_successfully(self):
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
                    {'id': 1, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                    {'id': 2, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                    {'id': 3, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0}]}]}
        probes_metadata_2 = {
            'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
            'shanks': [
                {'shank_id': 0, 'electrodes': [
                    {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                    {'id': 1, 'rel_x': 40, 'rel_y': 0, 'rel_z': 0}]},
                {'shank_id': 1, 'electrodes': [
                    {'id': 32, 'rel_x': 0.0, 'rel_y': 300.0, 'rel_z': 0.0},
                    {'id': 33, 'rel_x': 40.0, 'rel_y': 300.0, 'rel_z': 0.0}]},
                {'shank_id': 2, 'electrodes': [
                    {'id': 64, 'rel_x': 0.0, 'rel_y': 600.0, 'rel_z': 0.0},
                    {'id': 65, 'rel_x': 40.0, 'rel_y': 600.0, 'rel_z': 0.0}, ]},
                {'shank_id': 3, 'electrodes': [
                    {'id': 96, 'rel_x': 0.0, 'rel_y': 900.0, 'rel_z': 0.0},
                    {'id': 97, 'rel_x': 40.0, 'rel_y': 900.0, 'rel_z': 0.0}]}]}

        fl_shanks_electrode_manager = FlShanksElectrodeManager(
            probes_metadata=[probes_metadata_1, probes_metadata_2],
            electrode_groups_metadata=electrode_groups_metadata
        )
        fl_shanks_elecrodes_dict = fl_shanks_electrode_manager.get_fl_shanks_electrodes_dict()

        self.assertIsInstance(fl_shanks_elecrodes_dict, dict)
        self.assertIsInstance(fl_shanks_elecrodes_dict[probes_metadata_1['probe_type']], list)
        self.assertIsInstance(fl_shanks_elecrodes_dict[probes_metadata_1['probe_type']][0], FlShanksElectrode)

        self.assertEqual(len(fl_shanks_elecrodes_dict), 2)
        self.assertEqual(len(fl_shanks_elecrodes_dict[probes_metadata_1['probe_type']]), 4)
        self.assertEqual(len(fl_shanks_elecrodes_dict[probes_metadata_2['probe_type']]), 8)

        self.assertEqual(fl_shanks_elecrodes_dict[probes_metadata_1['probe_type']][0].shanks_electrode_id, 0)
        self.assertEqual(fl_shanks_elecrodes_dict[probes_metadata_1['probe_type']][0].rel_x, 11)
        self.assertEqual(fl_shanks_elecrodes_dict[probes_metadata_1['probe_type']][0].rel_y, 22)
        self.assertEqual(fl_shanks_elecrodes_dict[probes_metadata_1['probe_type']][0].rel_z, 33)

    @should_raise(TypeError)
    def test_fl_shanks_electrode_manager_failed_due_to_None_param(self):
        FlShanksElectrodeManager(
            probes_metadata=None,
            electrode_groups_metadata=None
        )
