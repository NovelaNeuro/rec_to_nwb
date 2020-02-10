import os
from unittest import TestCase

from src.datamigration.nwb_builder.builders.electrode_extension_builder import ElectrodeExtensionBuilder
from src.datamigration.nwb_builder.creators.electrode_metadata_extension_creator import \
    ElectrodesMetadataExtensionCreator

from src.datamigration.header.module.header import Header

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

        cls.header = Header(str(path) + '/res/nwb_elements_builder_test/header.xml')

        cls.electrode_extension_builder = ElectrodeExtensionBuilder(
            probes_metadata=probes,
            electrode_groups_metadata=metadata,
            header=cls.header
        )

        cls.electrodes_metadata_extension, cls.electrodes_header_extension = cls.electrode_extension_builder.build()

    def test_build_successfulReturn_true(self):
        self.assertIsNotNone(self.electrodes_metadata_extension)
        self.assertIsNotNone(self.electrodes_metadata_extension.rel_x)
        self.assertIsNotNone(self.electrodes_metadata_extension.rel_y)
        self.assertIsNotNone(self.electrodes_metadata_extension.rel_z)

        self.assertIsNotNone(self.electrodes_header_extension)

    def test_build_returnCorrectValues_true(self):
        self.assertEqual(self.electrodes_metadata_extension.rel_x[0], 0)
        self.assertEqual(self.electrodes_metadata_extension.rel_y[0], 0)
        self.assertEqual(self.electrodes_metadata_extension.rel_z[0], 0)
        self.assertEqual(self.electrodes_header_extension[0], '81')

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
