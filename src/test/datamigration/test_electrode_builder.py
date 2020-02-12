import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dateutil.tz import tzlocal
from hdmf.common import DynamicTable, VectorData, ElementIdentifiers
from pynwb import NWBFile

from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.nwb_builder.builders.electrode_builder import ElectrodeBuilder

path = os.path.dirname(os.path.abspath(__file__))


class TestElectrodeBuilder(TestCase):

    @classmethod
    def setUpClass(cls):
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

        cls.electrodes_builder = ElectrodeBuilder(probes, metadata)

        cls.nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        cls.mock_eg_1 = Mock()
        cls.mock_eg_2 = Mock()
        cls.mock_eg_1.__class__ = FLElectrodeGroup
        cls.mock_eg_2.__class__ = FLElectrodeGroup
        cls.mock_eg_1.name = 'FLElectrodeGroup1'
        cls.mock_eg_2.name = 'FLElectrodeGroup2'
        electrode_group_object_dict = {0: cls.mock_eg_1, 1: cls.mock_eg_2}

        cls.electrodes_builder.build(
            nwb_content=cls.nwb_file,
            electrode_group_dict=electrode_group_object_dict,
        )

    def test_build_correctObjectLength_true(self):
        self.assertEqual(12, len(self.nwb_file.electrodes))

    def test_build_returnCorrectType_true(self):
        self.assertIsInstance(self.nwb_file.electrodes, DynamicTable)

        self.assertIsInstance(self.nwb_file.electrodes['x'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['y'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['z'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['imp'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['location'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['filtering'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['group'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['group_name'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes.id, ElementIdentifiers)
        self.assertIsInstance(self.nwb_file.electrodes.description, str)

        self.assertIsInstance(self.nwb_file.electrodes[0][0], int)
        self.assertIsInstance(self.nwb_file.electrodes[0][1], float)
        self.assertIsInstance(self.nwb_file.electrodes[0][2], float)
        self.assertIsInstance(self.nwb_file.electrodes[0][3], float)
        self.assertIsInstance(self.nwb_file.electrodes[0][4], float)
        self.assertIsInstance(self.nwb_file.electrodes[0][5], str)
        self.assertIsInstance(self.nwb_file.electrodes[0][6], str)
        self.assertIsInstance(self.nwb_file.electrodes[0][7], FLElectrodeGroup)
        self.assertIsInstance(self.nwb_file.electrodes[0][8], str)

    def test_build_returnCorrectValues_true(self):
        self.assertEqual(self.nwb_file.electrodes[0][0], 0)
        self.assertEqual(self.nwb_file.electrodes[1][0], 1)

        self.assertEqual(self.nwb_file.electrodes[0][1], 0.0)
        self.assertEqual(self.nwb_file.electrodes[1][1], 0.0)

        self.assertEqual(self.nwb_file.electrodes[0][2], 0.0)
        self.assertEqual(self.nwb_file.electrodes[1][2], 0.0)

        self.assertEqual(self.nwb_file.electrodes[0][3], 0.0)
        self.assertEqual(self.nwb_file.electrodes[1][3], 0.0)

        self.assertEqual(self.nwb_file.electrodes[0][4], 0.0)
        self.assertEqual(self.nwb_file.electrodes[1][4], 0.0)

        self.assertEqual(self.nwb_file.electrodes[0][5], 'None')
        self.assertEqual(self.nwb_file.electrodes[1][5], 'None')

        self.assertEqual(self.nwb_file.electrodes[0][6], 'None')
        self.assertEqual(self.nwb_file.electrodes[1][6], 'None')

        self.assertEqual(self.nwb_file.electrodes[0][7], self.mock_eg_1)
        self.assertEqual(self.nwb_file.electrodes[1][7], self.mock_eg_1)

        self.assertEqual(self.nwb_file.electrodes[0][8], 'FLElectrodeGroup1')
        self.assertEqual(self.nwb_file.electrodes[1][8], 'FLElectrodeGroup1')