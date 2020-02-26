import os
from unittest import TestCase
from unittest.mock import Mock

from ndx_franklab_novela.fl_electrode_group import FLElectrodeGroup
from ndx_franklab_novela.probe import Probe
from src.datamigration.nwb.components.electrode_group.lf_electrode_group_manager import FlElectrodeGroupManager
from src.datamigration.nwb.components.electrode_group.lf_fl_electrode_group import LfFLElectrodeGroup

path = os.path.dirname(os.path.abspath(__file__))


class TestFlElectrodeGroupManager(TestCase):

    @classmethod
    def setUpClass(cls):

        cls.electrode_groups_metadata_1 = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'}
        cls.electrode_groups_metadata_2 = {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}
        electrode_groups_metadata = [ cls.electrode_groups_metadata_1, cls.electrode_groups_metadata_2]

        cls.mock_probe_1 = Mock(spec=Probe)
        cls.mock_probe_2 = Mock(spec=Probe)
        cls.probes = [cls.mock_probe_1, cls.mock_probe_2]

        cls.fl_electrode_group_manager = FlElectrodeGroupManager(
            electrode_groups_metadata=electrode_groups_metadata
        )

        cls.lf_fl_electrode_groups = cls.fl_electrode_group_manager.get_lf_fl_electrode_groups(
            probes=cls.probes
        )

    def test_build_successfulReturn_true(self):
        self.assertIsNotNone(self.lf_fl_electrode_groups)

    def test_build_returnCorrectValues_true(self):
        self.assertEqual(self.lf_fl_electrode_groups[0].metadata, self.electrode_groups_metadata_1)
        self.assertEqual(self.lf_fl_electrode_groups[0].device, self.mock_probe_1)

        self.assertEqual(self.lf_fl_electrode_groups[1].metadata, self.electrode_groups_metadata_2)
        self.assertEqual(self.lf_fl_electrode_groups[1].device, self.mock_probe_2)

    def test_build_correctObjectLength_true(self):
        self.assertEqual(2, len(self.lf_fl_electrode_groups))

    def test_build_returnCorrectType_true(self):
        self.assertIsInstance(self.lf_fl_electrode_groups, list)

        self.assertIsInstance(self.lf_fl_electrode_groups[0], LfFLElectrodeGroup)
        self.assertIsInstance(self.lf_fl_electrode_groups[0].metadata, dict)
        self.assertIsInstance(self.lf_fl_electrode_groups[0].device, Probe)

        self.assertIsInstance(self.lf_fl_electrode_groups[1], LfFLElectrodeGroup)
        self.assertIsInstance(self.lf_fl_electrode_groups[1].metadata, dict)
        self.assertIsInstance(self.lf_fl_electrode_groups[1].device, Probe)


