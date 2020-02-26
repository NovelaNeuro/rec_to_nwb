import os
from unittest import TestCase

from src.datamigration.nwb.components.device.lf_probe import LfProbe
from src.datamigration.nwb.components.device.lf_probe_manager import LfProbeManager

path = os.path.dirname(os.path.abspath(__file__))


class TestLfProbeManager(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.electrode_groups_metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}]

        cls.probes_metadata_1 = {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1, 'shanks': [
                {'shank_id': 0, 'electrodes': [
                    {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                    {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                    {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                    {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]}
        cls.probes_metadata_2 = {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4, 'shanks': [
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
        cls.probes_metadata = [cls.probes_metadata_1, cls.probes_metadata_2]

        cls.lf_probe_manager = LfProbeManager(
            probes_metadata=cls.probes_metadata,
            electrode_groups_metadata=cls.electrode_groups_metadata
        )
        cls.lf_probes_list = cls.lf_probe_manager.get_lf_probes_list()

    def test_build_successfulReturn_true(self):
        self.assertIsNotNone(self.lf_probes_list)

    def test_build_returnCorrectValues_true(self):
        self.assertEqual(self.lf_probes_list[0].metadata, self.probes_metadata_1)
        self.assertEqual(self.lf_probes_list[0].probe_id, 0)

        self.assertEqual(self.lf_probes_list[1].metadata, self.probes_metadata_2)
        self.assertEqual(self.lf_probes_list[1].probe_id, 1)

    def test_build_correctObjectLength_true(self):
        self.assertEqual(2, len(self.lf_probes_list))

    def test_build_returnCorrectType_true(self):
        self.assertIsInstance(self.lf_probes_list, list)

        self.assertIsInstance(self.lf_probes_list[0], LfProbe)
        self.assertIsInstance(self.lf_probes_list[0].metadata, dict)
        self.assertIsInstance(self.lf_probes_list[0].probe_id, int)

        self.assertIsInstance(self.lf_probes_list[1], LfProbe)
        self.assertIsInstance(self.lf_probes_list[1].metadata, dict)
        self.assertIsInstance(self.lf_probes_list[1].probe_id, int)
