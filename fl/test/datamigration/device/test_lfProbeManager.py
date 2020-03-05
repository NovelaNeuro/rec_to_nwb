import os
from unittest import TestCase
from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_in_init_exception import NoneParamInInitException
from fl.datamigration.nwb.components.device.fl_probe import LfProbe
from fl.datamigration.nwb.components.device.fl_probe_manager import LfProbeManager

path = os.path.dirname(os.path.abspath(__file__))


class TestLfProbeManager(TestCase):

    def setUp(self):
        self.electrode_groups_metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}]

        self.probes_metadata_1 = {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1, 'shanks': [
                {'shank_id': 0, 'electrodes': [
                    {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                    {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                    {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                    {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]}
        self.probes_metadata_2 = {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4, 'shanks': [
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
        self.probes_metadata = [self.probes_metadata_1, self.probes_metadata_2]

    def test_manager_builds_LfProbes_successfully(self):
        fl_probe_manager = LfProbeManager(
            probes_metadata=self.probes_metadata,
            electrode_groups_metadata=self.electrode_groups_metadata
        )

        fl_probes_list = fl_probe_manager.get_fl_probes_list()

        self.assertEqual(2, len(fl_probes_list))

        self.assertIsInstance(fl_probes_list[0], LfProbe)
        self.assertIsInstance(fl_probes_list[0].metadata, dict)
        self.assertIsInstance(fl_probes_list[0].probe_id, int)
        self.assertEqual(fl_probes_list[0].metadata, self.probes_metadata_1)
        self.assertEqual(fl_probes_list[0].probe_id, 0)

        self.assertIsInstance(fl_probes_list[1], LfProbe)
        self.assertIsInstance(fl_probes_list[1].metadata, dict)
        self.assertIsInstance(fl_probes_list[1].probe_id, int)
        self.assertEqual(fl_probes_list[1].metadata, self.probes_metadata_2)
        self.assertEqual(fl_probes_list[1].probe_id, 1)

    @should_raise(NoneParamInInitException)
    def test_manager_fails_creating_LfProbes_due_to_None_probe_metadata(self):
        fl_probe_manager = LfProbeManager(
            probes_metadata=None,
            electrode_groups_metadata=self.electrode_groups_metadata
        )

        fl_probe_manager.get_fl_probes_list()

    @should_raise(NoneParamInInitException)
    def test_manager_fails_creating_LfProbes_due_to_None_electrode_group_metadata(self):
        fl_probe_manager = LfProbeManager(
            probes_metadata=self.probes_metadata,
            electrode_groups_metadata=None
        )

        fl_probe_manager.get_fl_probes_list()