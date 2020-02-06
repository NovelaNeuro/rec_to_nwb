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
            {'id': 0, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}]
        probes = [{'probe_type': 'tetrode_12.5', 'probe_description': 'four wire electrode', 'num_shanks': 1,
                   'contact_size': 12.5, 'shanks': [{'shank_id': 0,
                                                     'electrodes': [{'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                                                                    {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                                                                    {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                                                                    {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]},
                  {'probe_type': '32c-2s8mm6cm-20um-40um-dl', 'probe_description': '32 channel polyimide probe',
                   'num_shanks': 2, 'contact_size': 20.0, 'shanks': [{'shank_id': 0, 'electrodes': [
                      {'id': 0, 'rel_x': 20, 'rel_y': 0, 'rel_z': 0}, {'id': 1, 'rel_x': 60, 'rel_y': 0, 'rel_z': 0},
                      {'id': 2, 'rel_x': 100, 'rel_y': 0, 'rel_z': 0}, {'id': 3, 'rel_x': 140, 'rel_y': 0, 'rel_z': 0},
                      {'id': 4, 'rel_x': 180, 'rel_y': 0, 'rel_z': 0}, {'id': 5, 'rel_x': 220, 'rel_y': 0, 'rel_z': 0},
                      {'id': 6, 'rel_x': 260, 'rel_y': 0, 'rel_z': 0}, {'id': 7, 'rel_x': 300, 'rel_y': 0, 'rel_z': 0},
                      {'id': 8, 'rel_x': 340, 'rel_y': 0, 'rel_z': 0}, {'id': 9, 'rel_x': 380, 'rel_y': 0, 'rel_z': 0},
                      {'id': 10, 'rel_x': 420, 'rel_y': 0, 'rel_z': 0},
                      {'id': 11, 'rel_x': 460, 'rel_y': 0, 'rel_z': 0},
                      {'id': 12, 'rel_x': 500, 'rel_y': 0, 'rel_z': 0},
                      {'id': 13, 'rel_x': 540, 'rel_y': 0, 'rel_z': 0},
                      {'id': 14, 'rel_x': 580, 'rel_y': 0, 'rel_z': 0},
                      {'id': 15, 'rel_x': 620, 'rel_y': 0, 'rel_z': 0}]}, {'shank_id': 1, 'electrodes': [
                      {'id': 16, 'rel_x': 20, 'rel_y': 250, 'rel_z': 0},
                      {'id': 17, 'rel_x': 60, 'rel_y': 300, 'rel_z': 0},
                      {'id': 18, 'rel_x': 100, 'rel_y': 300, 'rel_z': 0},
                      {'id': 19, 'rel_x': 140, 'rel_y': 300, 'rel_z': 0},
                      {'id': 20, 'rel_x': 180, 'rel_y': 300, 'rel_z': 0},
                      {'id': 21, 'rel_x': 220, 'rel_y': 300, 'rel_z': 0},
                      {'id': 22, 'rel_x': 260, 'rel_y': 300, 'rel_z': 0},
                      {'id': 23, 'rel_x': 300, 'rel_y': 300, 'rel_z': 0},
                      {'id': 24, 'rel_x': 340, 'rel_y': 300, 'rel_z': 0},
                      {'id': 25, 'rel_x': 380, 'rel_y': 300, 'rel_z': 0},
                      {'id': 26, 'rel_x': 420, 'rel_y': 300, 'rel_z': 0},
                      {'id': 27, 'rel_x': 460, 'rel_y': 300, 'rel_z': 0},
                      {'id': 28, 'rel_x': 500, 'rel_y': 300, 'rel_z': 0},
                      {'id': 29, 'rel_x': 540, 'rel_y': 300, 'rel_z': 0},
                      {'id': 30, 'rel_x': 580, 'rel_y': 300, 'rel_z': 0},
                      {'id': 31, 'rel_x': 620, 'rel_y': 300, 'rel_z': 0}]}]},
                  {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'probe_description': '128 channel polyimide probe',
                   'num_shanks': 4, 'contact_size': 20.0, 'shanks': [{'shank_id': 0, 'electrodes': [
                      {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}, {'id': 1, 'rel_x': 40, 'rel_y': 0, 'rel_z': 0},
                      {'id': 2, 'rel_x': 80, 'rel_y': 0, 'rel_z': 0}, {'id': 3, 'rel_x': 120, 'rel_y': 0, 'rel_z': 0},
                      {'id': 4, 'rel_x': 160, 'rel_y': 0, 'rel_z': 0}, {'id': 5, 'rel_x': 200, 'rel_y': 0, 'rel_z': 0},
                      {'id': 6, 'rel_x': 240, 'rel_y': 0, 'rel_z': 0}, {'id': 7, 'rel_x': 280, 'rel_y': 0, 'rel_z': 0},
                      {'id': 8, 'rel_x': 320, 'rel_y': 0, 'rel_z': 0}, {'id': 9, 'rel_x': 360, 'rel_y': 0, 'rel_z': 0},
                      {'id': 10, 'rel_x': 400, 'rel_y': 0, 'rel_z': 0},
                      {'id': 11, 'rel_x': 440, 'rel_y': 0, 'rel_z': 0},
                      {'id': 12, 'rel_x': 480, 'rel_y': 0, 'rel_z': 0},
                      {'id': 13, 'rel_x': 520, 'rel_y': 0, 'rel_z': 0},
                      {'id': 14, 'rel_x': 560, 'rel_y': 0, 'rel_z': 0},
                      {'id': 15, 'rel_x': 600, 'rel_y': 0, 'rel_z': 0},
                      {'id': 16, 'rel_x': 640, 'rel_y': 0, 'rel_z': 0},
                      {'id': 17, 'rel_x': 680, 'rel_y': 0, 'rel_z': 0},
                      {'id': 18, 'rel_x': 720, 'rel_y': 0, 'rel_z': 0},
                      {'id': 19, 'rel_x': 760, 'rel_y': 0, 'rel_z': 0},
                      {'id': 20, 'rel_x': 800, 'rel_y': 0, 'rel_z': 0},
                      {'id': 21, 'rel_x': 840, 'rel_y': 0, 'rel_z': 0},
                      {'id': 22, 'rel_x': 880, 'rel_y': 0, 'rel_z': 0},
                      {'id': 23, 'rel_x': 920, 'rel_y': 0, 'rel_z': 0},
                      {'id': 24, 'rel_x': 960, 'rel_y': 0, 'rel_z': 0},
                      {'id': 25, 'rel_x': 1000, 'rel_y': 0, 'rel_z': 0},
                      {'id': 26, 'rel_x': 1040, 'rel_y': 0, 'rel_z': 0},
                      {'id': 27, 'rel_x': 1080, 'rel_y': 0, 'rel_z': 0},
                      {'id': 28, 'rel_x': 1120, 'rel_y': 0, 'rel_z': 0},
                      {'id': 29, 'rel_x': 1160, 'rel_y': 0, 'rel_z': 0},
                      {'id': 30, 'rel_x': 1200, 'rel_y': 300, 'rel_z': 0},
                      {'id': 31, 'rel_x': 1240, 'rel_y': 0, 'rel_z': 0}]}, {'shank_id': 1, 'electrodes': [
                      {'id': 32, 'rel_x': 0, 'rel_y': 300, 'rel_z': 0},
                      {'id': 33, 'rel_x': 40, 'rel_y': 300, 'rel_z': 0},
                      {'id': 34, 'rel_x': 80, 'rel_y': 300, 'rel_z': 0},
                      {'id': 35, 'rel_x': 120, 'rel_y': 300, 'rel_z': 0},
                      {'id': 36, 'rel_x': 160, 'rel_y': 300, 'rel_z': 0},
                      {'id': 37, 'rel_x': 200, 'rel_y': 300, 'rel_z': 0},
                      {'id': 38, 'rel_x': 240, 'rel_y': 300, 'rel_z': 0},
                      {'id': 39, 'rel_x': 280, 'rel_y': 300, 'rel_z': 0},
                      {'id': 40, 'rel_x': 320, 'rel_y': 300, 'rel_z': 0},
                      {'id': 41, 'rel_x': 360, 'rel_y': 300, 'rel_z': 0},
                      {'id': 42, 'rel_x': 400, 'rel_y': 300, 'rel_z': 0},
                      {'id': 43, 'rel_x': 440, 'rel_y': 300, 'rel_z': 0},
                      {'id': 44, 'rel_x': 480, 'rel_y': 300, 'rel_z': 0},
                      {'id': 45, 'rel_x': 520, 'rel_y': 300, 'rel_z': 0},
                      {'id': 46, 'rel_x': 560, 'rel_y': 300, 'rel_z': 0},
                      {'id': 47, 'rel_x': 600, 'rel_y': 300, 'rel_z': 0},
                      {'id': 48, 'rel_x': 640, 'rel_y': 300, 'rel_z': 0},
                      {'id': 49, 'rel_x': 680, 'rel_y': 300, 'rel_z': 0},
                      {'id': 50, 'rel_x': 720, 'rel_y': 300, 'rel_z': 0},
                      {'id': 51, 'rel_x': 760, 'rel_y': 300, 'rel_z': 0},
                      {'id': 52, 'rel_x': 800, 'rel_y': 300, 'rel_z': 0},
                      {'id': 53, 'rel_x': 840, 'rel_y': 300, 'rel_z': 0},
                      {'id': 54, 'rel_x': 880, 'rel_y': 300, 'rel_z': 0},
                      {'id': 55, 'rel_x': 920, 'rel_y': 300, 'rel_z': 0},
                      {'id': 56, 'rel_x': 960, 'rel_y': 300, 'rel_z': 0},
                      {'id': 57, 'rel_x': 1000, 'rel_y': 300, 'rel_z': 0},
                      {'id': 58, 'rel_x': 1040, 'rel_y': 300, 'rel_z': 0},
                      {'id': 59, 'rel_x': 1080, 'rel_y': 300, 'rel_z': 0},
                      {'id': 60, 'rel_x': 1120, 'rel_y': 300, 'rel_z': 0},
                      {'id': 61, 'rel_x': 1160, 'rel_y': 300, 'rel_z': 0},
                      {'id': 62, 'rel_x': 1200, 'rel_y': 300, 'rel_z': 0},
                      {'id': 63, 'rel_x': 1240, 'rel_y': 300, 'rel_z': 0}]}, {'shank_id': 2, 'electrodes': [
                      {'id': 64, 'rel_x': 0, 'rel_y': 600, 'rel_z': 0},
                      {'id': 65, 'rel_x': 40, 'rel_y': 600, 'rel_z': 0},
                      {'id': 66, 'rel_x': 80, 'rel_y': 600, 'rel_z': 0},
                      {'id': 67, 'rel_x': 120, 'rel_y': 600, 'rel_z': 0},
                      {'id': 68, 'rel_x': 160, 'rel_y': 600, 'rel_z': 0},
                      {'id': 69, 'rel_x': 200, 'rel_y': 600, 'rel_z': 0},
                      {'id': 70, 'rel_x': 240, 'rel_y': 600, 'rel_z': 0},
                      {'id': 71, 'rel_x': 280, 'rel_y': 600, 'rel_z': 0},
                      {'id': 72, 'rel_x': 320, 'rel_y': 600, 'rel_z': 0},
                      {'id': 73, 'rel_x': 360, 'rel_y': 600, 'rel_z': 0},
                      {'id': 74, 'rel_x': 400, 'rel_y': 600, 'rel_z': 0},
                      {'id': 75, 'rel_x': 440, 'rel_y': 600, 'rel_z': 0},
                      {'id': 76, 'rel_x': 480, 'rel_y': 600, 'rel_z': 0},
                      {'id': 77, 'rel_x': 520, 'rel_y': 600, 'rel_z': 0},
                      {'id': 78, 'rel_x': 560, 'rel_y': 600, 'rel_z': 0},
                      {'id': 79, 'rel_x': 600, 'rel_y': 600, 'rel_z': 0},
                      {'id': 80, 'rel_x': 640, 'rel_y': 600, 'rel_z': 0},
                      {'id': 81, 'rel_x': 680, 'rel_y': 600, 'rel_z': 0},
                      {'id': 82, 'rel_x': 720, 'rel_y': 600, 'rel_z': 0},
                      {'id': 83, 'rel_x': 760, 'rel_y': 600, 'rel_z': 0},
                      {'id': 84, 'rel_x': 800, 'rel_y': 600, 'rel_z': 0},
                      {'id': 85, 'rel_x': 840, 'rel_y': 600, 'rel_z': 0},
                      {'id': 86, 'rel_x': 880, 'rel_y': 600, 'rel_z': 0},
                      {'id': 87, 'rel_x': 920, 'rel_y': 600, 'rel_z': 0},
                      {'id': 88, 'rel_x': 960, 'rel_y': 600, 'rel_z': 0},
                      {'id': 89, 'rel_x': 1000, 'rel_y': 600, 'rel_z': 0},
                      {'id': 90, 'rel_x': 1040, 'rel_y': 600, 'rel_z': 0},
                      {'id': 91, 'rel_x': 1080, 'rel_y': 600, 'rel_z': 0},
                      {'id': 92, 'rel_x': 1120, 'rel_y': 600, 'rel_z': 0},
                      {'id': 93, 'rel_x': 1160, 'rel_y': 600, 'rel_z': 0},
                      {'id': 94, 'rel_x': 1200, 'rel_y': 600, 'rel_z': 0},
                      {'id': 95, 'rel_x': 1240, 'rel_y': 600, 'rel_z': 0}]}, {'shank_id': 3, 'electrodes': [
                      {'id': 96, 'rel_x': 0, 'rel_y': 900, 'rel_z': 0},
                      {'id': 97, 'rel_x': 40, 'rel_y': 900, 'rel_z': 0},
                      {'id': 98, 'rel_x': 80, 'rel_y': 900, 'rel_z': 0},
                      {'id': 99, 'rel_x': 120, 'rel_y': 900, 'rel_z': 0},
                      {'id': 100, 'rel_x': 160, 'rel_y': 900, 'rel_z': 0},
                      {'id': 101, 'rel_x': 200, 'rel_y': 900, 'rel_z': 0},
                      {'id': 102, 'rel_x': 240, 'rel_y': 900, 'rel_z': 0},
                      {'id': 103, 'rel_x': 280, 'rel_y': 900, 'rel_z': 0},
                      {'id': 104, 'rel_x': 320, 'rel_y': 900, 'rel_z': 0},
                      {'id': 105, 'rel_x': 360, 'rel_y': 900, 'rel_z': 0},
                      {'id': 106, 'rel_x': 400, 'rel_y': 900, 'rel_z': 0},
                      {'id': 107, 'rel_x': 440, 'rel_y': 900, 'rel_z': 0},
                      {'id': 108, 'rel_x': 480, 'rel_y': 900, 'rel_z': 0},
                      {'id': 109, 'rel_x': 520, 'rel_y': 900, 'rel_z': 0},
                      {'id': 110, 'rel_x': 560, 'rel_y': 900, 'rel_z': 0},
                      {'id': 111, 'rel_x': 600, 'rel_y': 900, 'rel_z': 0},
                      {'id': 112, 'rel_x': 640, 'rel_y': 900, 'rel_z': 0},
                      {'id': 113, 'rel_x': 680, 'rel_y': 900, 'rel_z': 0},
                      {'id': 114, 'rel_x': 720, 'rel_y': 900, 'rel_z': 0},
                      {'id': 115, 'rel_x': 760, 'rel_y': 900, 'rel_z': 0},
                      {'id': 116, 'rel_x': 800, 'rel_y': 900, 'rel_z': 0},
                      {'id': 117, 'rel_x': 840, 'rel_y': 900, 'rel_z': 0},
                      {'id': 118, 'rel_x': 880, 'rel_y': 900, 'rel_z': 0},
                      {'id': 119, 'rel_x': 920, 'rel_y': 900, 'rel_z': 0},
                      {'id': 120, 'rel_x': 960, 'rel_y': 900, 'rel_z': 0},
                      {'id': 121, 'rel_x': 1000, 'rel_y': 900, 'rel_z': 0},
                      {'id': 122, 'rel_x': 1040, 'rel_y': 900, 'rel_z': 0},
                      {'id': 123, 'rel_x': 1080, 'rel_y': 900, 'rel_z': 0},
                      {'id': 124, 'rel_x': 1120, 'rel_y': 900, 'rel_z': 0},
                      {'id': 125, 'rel_x': 1160, 'rel_y': 900, 'rel_z': 0},
                      {'id': 126, 'rel_x': 1200, 'rel_y': 900, 'rel_z': 0},
                      {'id': 127, 'rel_x': 1240, 'rel_y': 900, 'rel_z': 0}]}]}]

        self.electrodes_builder = ElectrodeBuilder(probes, metadata)

    def test_build_successful_creation(self):
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
        # ToDo Need idea how to test it with mock_nwb

        # then
        # self.assertEqual(256, len(electrodes))
        # self.assertIsInstance(electrodes[0], DynamicTable)
        # self.assertIsInstance(electrodes[1], DynamicTable)
