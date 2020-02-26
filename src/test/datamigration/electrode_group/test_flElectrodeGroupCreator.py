from unittest import TestCase
from unittest.mock import Mock

from ndx_franklab_novela.probe import Probe
from pynwb.device import Device

from src.datamigration.nwb.components.electrode_group.fl_electrode_group_creator import FlElectrodeGroupCreator
from src.datamigration.nwb.components.electrode_group.lf_fl_electrode_group import LfFLElectrodeGroup


class TestFlElectrodeGroupCreator(TestCase):

    @classmethod
    def setUpClass(cls):

        cls.mock_probe = Mock(spec=Probe)
        cls.mock_device = Mock(spec=Device)

        cls.mock_lf_fl_electrode_group_1 = Mock(spec=LfFLElectrodeGroup)
        cls.mock_lf_fl_electrode_group_1.metadata = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'ElectrodeGroup 1'}
        cls.mock_lf_fl_electrode_group_1.device = cls.mock_probe

        cls.mock_lf_fl_electrode_group_2 = Mock(spec=LfFLElectrodeGroup)
        cls.mock_lf_fl_electrode_group_2.device = cls.mock_device
        cls.mock_lf_fl_electrode_group_2.metadata = {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'ElectrodeGroup 2'}

        cls.fl_electrode_group_1 = FlElectrodeGroupCreator.create(cls.mock_lf_fl_electrode_group_1)
        cls.fl_electrode_group_2 = FlElectrodeGroupCreator.create(cls.mock_lf_fl_electrode_group_2)

    def test_createElectrodeGroup_successfulCreate_true(self):
        self.assertIsNotNone(self.fl_electrode_group_1)
        self.assertIsNotNone(self.fl_electrode_group_2)

    def test_createElectrodeGroup_returnCorrectValues_true(self):
        self.assertEqual(self.fl_electrode_group_1.name, 'electrode group 0')
        self.assertEqual(self.fl_electrode_group_1.location, 'mPFC')
        self.assertEqual(self.fl_electrode_group_1.description, 'ElectrodeGroup 1')
        self.assertEqual(self.fl_electrode_group_1.id, 0)
        self.assertEqual(self.fl_electrode_group_1.device, self.mock_probe)

        self.assertEqual(self.fl_electrode_group_2.name, 'electrode group 1')
        self.assertEqual(self.fl_electrode_group_2.location, 'mPFC')
        self.assertEqual(self.fl_electrode_group_2.description, 'ElectrodeGroup 2')
        self.assertEqual(self.fl_electrode_group_2.id, 1)
        self.assertEqual(self.fl_electrode_group_2.device, self.mock_device)

    def test_createElectrodeGroup_returnCorrectType_true(self):
        self.assertIsInstance(self.fl_electrode_group_1.name, str)
        self.assertIsInstance(self.fl_electrode_group_1.location, str)
        self.assertIsInstance(self.fl_electrode_group_1.description, str)
        self.assertIsInstance(self.fl_electrode_group_1.id, int)
        self.assertIsInstance(self.fl_electrode_group_1.device, Device)

        self.assertIsInstance(self.fl_electrode_group_2.name, str)
        self.assertIsInstance(self.fl_electrode_group_2.location, str)
        self.assertIsInstance(self.fl_electrode_group_2.description, str)
        self.assertIsInstance(self.fl_electrode_group_2.id, int)
        self.assertIsInstance(self.fl_electrode_group_2.device, Device)