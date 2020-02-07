import os
from unittest import TestCase

from src.datamigration.extension.probe import Probe
from src.datamigration.nwb_builder.builders.probes_dict_builder import ProbesDictBuilder

path = os.path.dirname(os.path.abspath(__file__))


class TestProbesDictBuilder(TestCase):

    def setUp(self):
        metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}]

        probes = [{'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
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

        self.probes_builder = ProbesDictBuilder(
            probes_metadata=probes,
            electrode_groups_metadata=metadata
        )
        self.probes_dict = self.probes_builder.build()

    def test_build_successfulReturn_true(self):
        self.assertIsNotNone(self.probes_dict)

    def test_build_returnCorrectValues_true(self):
        self.assertEqual(self.probes_dict[0].probe_type, 'tetrode_12.5')
        self.assertEqual(self.probes_dict[0].contact_size, 20.0)
        self.assertEqual(self.probes_dict[0].num_shanks, 1)
        self.assertEqual(self.probes_dict[0].id, 0)

        self.assertEqual(self.probes_dict[1].probe_type, '128c-4s8mm6cm-20um-40um-sl')
        self.assertEqual(self.probes_dict[1].contact_size, 20.0)
        self.assertEqual(self.probes_dict[1].num_shanks, 4)
        self.assertEqual(self.probes_dict[1].id, 1)

    def test_build_correctObjectLength_true(self):
        self.assertEqual(2, len(self.probes_dict))

    def test_build_returnCorrectType_true(self):
        self.assertIsInstance(self.probes_dict[0], Probe)
        self.assertIsInstance(self.probes_dict[0].probe_type, str)
        self.assertIsInstance(self.probes_dict[0].contact_size, float)
        self.assertIsInstance(self.probes_dict[0].num_shanks, int)
        self.assertIsInstance(self.probes_dict[0].id, int)

        self.assertIsInstance(self.probes_dict[1], Probe)
        self.assertIsInstance(self.probes_dict[1].probe_type, str)
        self.assertIsInstance(self.probes_dict[1].contact_size, float)
        self.assertIsInstance(self.probes_dict[1].num_shanks, int)
        self.assertIsInstance(self.probes_dict[1].id, int)
