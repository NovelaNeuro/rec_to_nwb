from unittest import TestCase

from src.datamigration.nwb.components.electrodes.electrode_ntrode_extension_creator import \
    ElectrodesNtrodeExtensionCreator


class TestElectrodesNtrodeExtensionCreator(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.metadata = [
            {'ntrode_id': 1, 'probe_id': 0, 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
            {'ntrode_id': 2, 'probe_id': 0, 'map': {0: 32, 1: 33, 2: 34, 3: 35, 4: 36}},
            {'ntrode_id': 3, 'probe_id': 1, 'map': {0: 64, 1: 65, 2: 66, 3: 67, 4: 68}},
            {'ntrode_id': 4, 'probe_id': 1, 'map': {0: 96, 1: 97, 2: 98, 3: 99, 4: 100}}
        ]

        cls.electrodes_ntrode_extension_creator = ElectrodesNtrodeExtensionCreator()

    def test_create_electrodes_ntrode_extension_returnCorrectValue_true(self):
        ntrode_extension = self.electrodes_ntrode_extension_creator.create_electrodes_ntrode_extension(self.metadata)
        self.assertIsInstance(ntrode_extension, list)
        self.assertIsInstance(ntrode_extension[0], int)

    def test_create_electrodes_ntrode_extension_returnCorrectType_true(self):
        ntrode_extension = self.electrodes_ntrode_extension_creator.create_electrodes_ntrode_extension(self.metadata)
        self.assertEqual(ntrode_extension, [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4])
        self.assertEqual(ntrode_extension[0], 1)
        self.assertEqual(ntrode_extension[-1], 4)