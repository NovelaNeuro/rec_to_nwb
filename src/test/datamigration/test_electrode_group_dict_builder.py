import os
from unittest import TestCase
from unittest.mock import Mock

from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.extension.probe import Probe
from src.datamigration.nwb_builder.builders.electrode_group_dict_builder import ElectrodeGroupDictBuilder

path = os.path.dirname(os.path.abspath(__file__))


class TestElectrodeGroupDictBuilder(TestCase):

    def setUp(self):
        metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}]

        self.electrode_group_builder = ElectrodeGroupDictBuilder(
            electrode_groups_metadata=metadata
        )

    def test_build_successful_creation(self):
        # given
        mock_1 = Mock()
        mock_2 = Mock()
        mock_1.__class__ = Probe
        mock_2.__class__ = Probe
        probes_object_dict = {0: mock_1, 1: mock_2}

        # when
        electrode_group_dict = self.electrode_group_builder.build(
            probes=probes_object_dict
        )

        # then
        self.assertEqual(2, len(electrode_group_dict))
        self.assertIsInstance(electrode_group_dict[0], FLElectrodeGroup)
        self.assertIsInstance(electrode_group_dict[1], FLElectrodeGroup)
