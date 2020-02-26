from unittest import TestCase
from unittest.mock import Mock

from ndx_franklab_novela.probe import Probe
from pynwb.device import Device

from src.datamigration.nwb.components.electrode_group.electrode_group_creator import ElectrodeGroupCreator


class TestElectrodeGroupCreator(TestCase):

    @classmethod
    def setUpClass(cls):
        metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'ElectrodeGroup 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl',
             'description': 'ElectrodeGroup 2'}
        ]

        cls.mock_probe = Mock(spec=Probe)
        cls.mock_device = Mock(spec=Device)

        cls.electrode_group_1 = ElectrodeGroupCreator.create_electrode_group(metadata[0], cls.mock_probe)
        cls.electrode_group_2 = ElectrodeGroupCreator.create_electrode_group(metadata[1], cls.mock_device)

    def test_createElectrodeGroup_successfulCreate_true(self):
        self.assertIsNotNone(self.electrode_group_1)
        self.assertIsNotNone(self.electrode_group_2)

    def test_createElectrodeGroup_returnCorrectValues_true(self):
        self.assertEqual(self.electrode_group_1.name, 'electrode group 0')
        self.assertEqual(self.electrode_group_1.location, 'mPFC')
        self.assertEqual(self.electrode_group_1.description, 'ElectrodeGroup 1')
        self.assertEqual(self.electrode_group_1.id, 0)
        self.assertEqual(self.electrode_group_1.device, self.mock_probe)

        self.assertEqual(self.electrode_group_2.name, 'electrode group 1')
        self.assertEqual(self.electrode_group_2.location, 'mPFC')
        self.assertEqual(self.electrode_group_2.description, 'ElectrodeGroup 2')
        self.assertEqual(self.electrode_group_2.id, 1)
        self.assertEqual(self.electrode_group_2.device, self.mock_device)

    def test_createElectrodeGroup_returnCorrectType_true(self):
        self.assertIsInstance(self.electrode_group_1.name, str)
        self.assertIsInstance(self.electrode_group_1.location, str)
        self.assertIsInstance(self.electrode_group_1.description, str)
        self.assertIsInstance(self.electrode_group_1.id, int)
        self.assertIsInstance(self.electrode_group_1.device, Device)

        self.assertIsInstance(self.electrode_group_2.name, str)
        self.assertIsInstance(self.electrode_group_2.location, str)
        self.assertIsInstance(self.electrode_group_2.description, str)
        self.assertIsInstance(self.electrode_group_2.id, int)
        self.assertIsInstance(self.electrode_group_2.device, Device)
