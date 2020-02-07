import os
from unittest import TestCase
from unittest.mock import Mock

from pynwb import NWBFile

from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.nwb_builder.builders.electrode_builder import ElectrodeBuilder

path = os.path.dirname(os.path.abspath(__file__))


class TestElectrodeBuilder(TestCase):

    def setUp(self):
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

        self.electrodes_builder = ElectrodeBuilder(probes, metadata)

    def test_build_successful_creation_true(self):
        # given
        mock_nwb = Mock()
        mock_nwb.__class__ = NWBFile

        mock_eg_1 = Mock()
        mock_eg_2 = Mock()
        mock_eg_1.__class__ = FLElectrodeGroup
        mock_eg_2.__class__ = FLElectrodeGroup
        electrode_group_object_dict = {0: mock_eg_1, 1: mock_eg_2}

        # when
        self.electrodes_builder.build(
            nwb_content=mock_nwb,
            electrode_group_dict=electrode_group_object_dict,
        )

        # then
        # print(mock_nwb.electrodes)
        # self.assertEqual(256, len(electrodes))
        # self.assertIsInstance(electrodes[0], DynamicTable)
        # self.assertIsInstance(electrodes[1], DynamicTable)
