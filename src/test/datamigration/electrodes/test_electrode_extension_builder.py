import os
from unittest import TestCase

from src.datamigration.header.module.header import Header
from src.datamigration.nwb.components.electrodes.electrode_extension_builder import ElectrodeExtensionBuilder
from src.datamigration.nwb.components.electrodes.electrode_metadata_extension_creator import \
    ElectrodesMetadataExtensionCreator

path = os.path.dirname(os.path.abspath(__file__))


class TestElectrodeExtensionsBuilder(TestCase):

    @classmethod
    def setUpClass(cls):
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

        ntrodes_metadata = [
            {'ntrode_id': 1, 'probe_id': 0, 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
            {'ntrode_id': 2, 'probe_id': 0, 'map': {0: 32, 1: 33, 2: 34, 3: 35, 4: 36}},
            {'ntrode_id': 3, 'probe_id': 1, 'map': {0: 64, 1: 65, 2: 66, 3: 67, 4: 68}},
            {'ntrode_id': 4, 'probe_id': 1, 'map': {0: 96, 1: 97, 2: 98, 3: 99, 4: 100}}
        ]

        cls.header = Header(str(path) + '/../res/nwb_elements_builder_test/header.xml')

        cls.electrode_extension_builder = ElectrodeExtensionBuilder(
            probes_metadata=probes,
            electrode_groups_metadata=metadata,
            header=cls.header,
            ntrodes_metadata=ntrodes_metadata
        )

        cls.electrodes_metadata_extension, cls.electrodes_header_extension, cls.electrodes_ntrodes_extension = \
            cls.electrode_extension_builder.build()

    def test_build_successfulReturn_true(self):
        self.assertIsNotNone(self.electrodes_metadata_extension)
        self.assertIsNotNone(self.electrodes_metadata_extension.rel_x)
        self.assertIsNotNone(self.electrodes_metadata_extension.rel_y)
        self.assertIsNotNone(self.electrodes_metadata_extension.rel_z)

        self.assertIsNotNone(self.electrodes_header_extension)

        self.assertIsNotNone(self.electrodes_ntrodes_extension)

    def test_build_returnCorrectValues_true(self):
        self.assertEqual(self.electrodes_metadata_extension.rel_x[0], 0)
        self.assertEqual(self.electrodes_metadata_extension.rel_y[0], 0)
        self.assertEqual(self.electrodes_metadata_extension.rel_z[0], 0)

        self.assertEqual(self.electrodes_header_extension[0], '81')

        self.assertEqual(self.electrodes_ntrodes_extension[0], 1)
        self.assertEqual(self.electrodes_ntrodes_extension[-1], 4)

    def test_build_returnCorrectObject_true(self):
        self.assertIsInstance(self.electrodes_metadata_extension, ElectrodesMetadataExtensionCreator)

        self.assertIsInstance(self.electrodes_metadata_extension.rel_x, list)
        self.assertIsInstance(self.electrodes_metadata_extension.rel_y, list)
        self.assertIsInstance(self.electrodes_metadata_extension.rel_z, list)
        self.assertIsInstance(self.electrodes_metadata_extension.rel_x[0], int)
        self.assertIsInstance(self.electrodes_metadata_extension.rel_y[0], int)
        self.assertIsInstance(self.electrodes_metadata_extension.rel_z[0], int)

        self.assertIsInstance(self.electrodes_header_extension, list)
        self.assertIsInstance(self.electrodes_header_extension[0], str)

        self.assertIsInstance(self.electrodes_ntrodes_extension, list)
        self.assertIsInstance(self.electrodes_ntrodes_extension[0], int)
