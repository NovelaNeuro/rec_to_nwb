import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dateutil.tz import tzlocal
from hdmf.common import DynamicTable, VectorData, ElementIdentifiers
from pynwb import NWBFile

from ndx_franklab_novela.fl_electrode_group import FLElectrodeGroup
from src.datamigration.nwb.components.electrodes.lf_electrode_manager import LfElectrodeManager

path = os.path.dirname(os.path.abspath(__file__))


class TestLfElectrodeManager(TestCase):

    @classmethod
    def setUpClass(cls):
        electrode_groups_metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}]

        probes_metadata = [{'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
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

        cls.lf_electrodes_manager = LfElectrodeManager(probes_metadata, electrode_groups_metadata)

        cls.mock_eg_1 = Mock()
        cls.mock_eg_2 = Mock()
        cls.mock_eg_1.__class__ = FLElectrodeGroup
        cls.mock_eg_2.__class__ = FLElectrodeGroup
        cls.mock_eg_1.name = 'FLElectrodeGroup1'
        cls.mock_eg_2.name = 'FLElectrodeGroup2'

        cls.lf_electrodes = cls.lf_electrodes_manager.get_lf_electrodes(
            electrode_groups=[cls.mock_eg_1, cls.mock_eg_2],
        )

    def test_build_correctObjectLength_true(self):
        self.assertEqual(12, len(self.lf_electrodes))

    def test_build_returnCorrectType_true(self):
        self.assertIsInstance(self.lf_electrodes, list)

        self.assertIsInstance(self.lf_electrodes[0].electrode_group, FLElectrodeGroup)
        self.assertIsInstance(self.lf_electrodes[1].electrode_group, FLElectrodeGroup)
        self.assertIsInstance(self.lf_electrodes[2].electrode_group, FLElectrodeGroup)
        self.assertIsInstance(self.lf_electrodes[3].electrode_group, FLElectrodeGroup)

        self.assertIsInstance(self.lf_electrodes[4].electrode_group, FLElectrodeGroup)

    def test_build_returnCorrectValues_true(self):
        self.assertEqual(self.lf_electrodes[0].electrode_group, self.mock_eg_1)
        self.assertEqual(self.lf_electrodes[1].electrode_group, self.mock_eg_1)
        self.assertEqual(self.lf_electrodes[2].electrode_group, self.mock_eg_1)
        self.assertEqual(self.lf_electrodes[3].electrode_group, self.mock_eg_1)

        self.assertEqual(self.lf_electrodes[4].electrode_group, self.mock_eg_2)
        self.assertEqual(self.lf_electrodes[5].electrode_group, self.mock_eg_2)
        self.assertEqual(self.lf_electrodes[6].electrode_group, self.mock_eg_2)
