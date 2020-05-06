from unittest import TestCase
from unittest.mock import Mock

from ndx_fl_novela.ntrode import NTrode
from pynwb.device import Device

from fl.processing.nwb.components.ntrodes.fl_ntrodes import FlNTrodes
from fl.processing.nwb.components.ntrodes.ntrodes_creator import NTrodesCreator


class TestNTrodesCreator(TestCase):

    @classmethod
    def setUpClass(cls):
        ntrode_creator = NTrodesCreator()

        cls.fl_ntrodes = Mock(spec=FlNTrodes)
        cls.fl_ntrodes.metadata = {'ntrode_id': 1, 'electrode_group_id': 2, 'bad_channels':[2,3] }
        cls.fl_ntrodes.map_list = [[1, 2], [3, 4], [5, 6]]
        cls.fl_ntrodes.bad_channels = [2, 3]
        cls.fl_ntrodes.device = Mock(spec=Device)

        cls.ntrode = ntrode_creator.create_ntrode(cls.fl_ntrodes)

    def test_createNTrode_successfulNodeCreation_true(self):
        self.assertIsInstance(self.ntrode, NTrode)

    def test_createNTrode_checkNodeCorrectValue_true(self):
        self.assertEqual(self.ntrode.name, 'ntrode 1')
        self.assertEqual(self.ntrode.description, '-')
        self.assertEqual(self.ntrode.location, '-')
        self.assertEqual(self.ntrode.device,  self.fl_ntrodes.device)
        self.assertEqual(self.ntrode.ntrode_id, 1)
        self.assertEqual(self.ntrode.electrode_group_id, 2)
        self.assertEqual(self.ntrode.map, [[1, 2], [3, 4], [5, 6]])

    def test_createNTrode_checkNodeCorrectType_true(self):
        self.assertIsInstance(self.ntrode.name, str)
        self.assertIsInstance(self.ntrode.description, str)
        self.assertIsInstance(self.ntrode.location, str)
        self.assertIsInstance(self.ntrode.device, Device)
        self.assertIsInstance(self.ntrode.ntrode_id, int)
        self.assertIsInstance(self.ntrode.electrode_group_id, int)
        self.assertIsInstance(self.ntrode.map, list)