from unittest import TestCase

from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.electrodes.electrode_ntrode_extension_creator import \
    ElectrodesNtrodeExtensionCreator


class TestElectrodesNtrodeExtensionCreator(TestCase):

    def test_electrodes_ntrode_extension_creator_create_ntrode_extension_successfully(self):
        metadata = [
            {'ntrode_id': 1, 'probe_id': 0, 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
            {'ntrode_id': 2, 'probe_id': 0, 'map': {0: 32, 1: 33, 2: 34, 3: 35, 4: 36}},
            {'ntrode_id': 3, 'probe_id': 1, 'map': {0: 64, 1: 65, 2: 66, 3: 67, 4: 68}},
            {'ntrode_id': 4, 'probe_id': 1, 'map': {0: 96, 1: 97, 2: 98, 3: 99, 4: 100}}
        ]

        electrodes_ntrode_extension_creator = ElectrodesNtrodeExtensionCreator()

        ntrode_extension = electrodes_ntrode_extension_creator.create_electrodes_ntrode_extension(metadata)

        self.assertIsInstance(ntrode_extension, list)
        self.assertIsInstance(ntrode_extension[0], int)
        self.assertEqual(ntrode_extension, [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4])
        self.assertEqual(ntrode_extension[0], 1)
        self.assertEqual(ntrode_extension[-1], 4)

    @should_raise(NoneParamException)
    def test_electrodes_ntrode_extension_creator_failed_create_ntrode_extension_due_to_None_param(self):
        electrodes_ntrode_extension_creator = ElectrodesNtrodeExtensionCreator()
        electrodes_ntrode_extension_creator.create_electrodes_ntrode_extension(None)
