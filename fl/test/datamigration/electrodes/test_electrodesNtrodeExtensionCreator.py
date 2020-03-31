from unittest import TestCase

from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.electrodes.electrode_ntrode_extension_creator import \
    ElectrodesNtrodeExtensionCreator


class TestElectrodesNtrodeExtensionCreator(TestCase):

    def test_electrodes_ntrode_extension_creator_create_ntrode_extension_ntrode_id_successfully(self):
        metadata = [
            {'ntrode_id': 1, 'probe_id': 0, 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
            {'ntrode_id': 2, 'probe_id': 0, 'map': {0: 32, 1: 33, 2: 34, 3: 35, 4: 36}},
            {'ntrode_id': 3, 'probe_id': 1, 'map': {0: 64, 1: 65, 2: 66, 3: 67, 4: 68}},
            {'ntrode_id': 4, 'probe_id': 1, 'map': {0: 96, 1: 97, 2: 98, 3: 99, 4: 100}}
        ]

        ntrode_extension_ntrode_id = ElectrodesNtrodeExtensionCreator().create_electrodes_ntrode_extension_ntrode_id(metadata)

        self.assertIsInstance(ntrode_extension_ntrode_id, list)
        self.assertIsInstance(ntrode_extension_ntrode_id[0], int)
        self.assertEqual(ntrode_extension_ntrode_id, [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4])
        self.assertEqual(ntrode_extension_ntrode_id[0], 1)
        self.assertEqual(ntrode_extension_ntrode_id[-1], 4)

    def test_electrodes_ntrode_extension_creator_create_ntrode_extension_bad_channels_successfully(self):
        metadata = [
            {'ntrode_id': 1, 'probe_id': 0, 'bad_channels': [0,2], 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
            {'ntrode_id': 2, 'probe_id': 0, 'bad_channels': [0,3], 'map': {0: 32, 1: 33, 2: 34, 3: 35, 4: 36}},
            {'ntrode_id': 3, 'probe_id': 1, 'bad_channels': [0,1], 'map': {0: 64, 1: 65, 2: 66, 3: 67, 4: 68}},
            {'ntrode_id': 4, 'probe_id': 1, 'bad_channels': [0,2,3], 'map': {0: 96, 1: 97, 2: 98, 3: 99, 4: 100}}
        ]

        ntrode_extension_bad_channels = ElectrodesNtrodeExtensionCreator().create_electrodes_ntrode_extension_bad_channels(metadata)

        self.assertIsInstance(ntrode_extension_bad_channels, list)
        self.assertIsInstance(ntrode_extension_bad_channels[0], bool)
        self.assertEqual(ntrode_extension_bad_channels, [True, False, True, False, False, True, False, False, True, False, True, True, False, False, False, True, False, True, True, False])
        self.assertEqual(ntrode_extension_bad_channels[0], True)
        self.assertEqual(ntrode_extension_bad_channels[-1], False)

    @should_raise(NoneParamException)
    def test_electrodes_ntrode_extension_creator_failed_create_ntrode_extension_ntrode_id_due_to_None_param(self):
        ElectrodesNtrodeExtensionCreator().create_electrodes_ntrode_extension_ntrode_id(None)

    @should_raise(NoneParamException)
    def test_electrodes_ntrode_extension_creator_failed_create_ntrode_extension_bad_channels_due_to_None_param(self):
        ElectrodesNtrodeExtensionCreator().create_electrodes_ntrode_extension_bad_channels(None)