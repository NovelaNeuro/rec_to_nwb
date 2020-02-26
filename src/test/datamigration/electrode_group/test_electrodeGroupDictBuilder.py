import os
from unittest import TestCase
from unittest.mock import Mock

from ndx_franklab_novela.fl_electrode_group import FLElectrodeGroup
from ndx_franklab_novela.probe import Probe

from src.datamigration.nwb.components.electrode_group.electrode_group_dict_builder import ElectrodeGroupDictBuilder

path = os.path.dirname(os.path.abspath(__file__))


class TestElectrodeGroupDictBuilder(TestCase):

    @classmethod
    def setUpClass(cls):
        metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}]

        mock_probe_1 = Mock(spec=Probe)
        mock_probe_2 = Mock(spec=Probe)
        probes_object_dict = {0: mock_probe_1, 1: mock_probe_2}

        cls.electrode_group_builder = ElectrodeGroupDictBuilder(
            electrode_groups_metadata=metadata
        )

        cls.electrode_group_dict = cls.electrode_group_builder.build(
            probes=probes_object_dict
        )

    def test_build_successfulReturn_true(self):
        self.assertIsNotNone(self.electrode_group_dict)

    def test_build_returnCorrectValues_true(self):
        self.assertEqual(self.electrode_group_dict[0].location, 'mPFC')
        self.assertEqual(self.electrode_group_dict[0].description, 'Probe 1')
        self.assertEqual(self.electrode_group_dict[0].id, 0)

        self.assertEqual(self.electrode_group_dict[1].location, 'mPFC')
        self.assertEqual(self.electrode_group_dict[1].description, 'Probe 2')
        self.assertEqual(self.electrode_group_dict[1].id, 1)

    def test_build_correctObjectLength_true(self):
        self.assertEqual(2, len(self.electrode_group_dict))

    def test_build_returnCorrectType_true(self):
        self.assertIsInstance(self.electrode_group_dict, dict)
        self.assertIsInstance(self.electrode_group_dict[0], FLElectrodeGroup)
        self.assertIsInstance(self.electrode_group_dict[1], FLElectrodeGroup)
        self.assertIsInstance(self.electrode_group_dict[1].location, str)
        self.assertIsInstance(self.electrode_group_dict[1].description, str)
        self.assertIsInstance(self.electrode_group_dict[1].device, Probe)
        self.assertIsInstance(self.electrode_group_dict[1].id, int)

