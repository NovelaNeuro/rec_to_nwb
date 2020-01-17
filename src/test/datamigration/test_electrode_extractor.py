import os
import unittest

import yaml

from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.electrode_extractor import ElectrodeExtractor


class TestMDAMigration(unittest.TestCase):

    @classmethod
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        header = Header(path + '/res/fl_lab_sample_header.xml')

        with open(path + '/res/probe_test.yml', 'r') as stream:
            probe_dict = yaml.safe_load(stream)
        probes = [probe_dict]
        self.extractor = ElectrodeExtractor(probes, header)
        self.electrodes = self.extractor.get_all_electrodes()

    def test_electrodes(self):
        self.assertEqual(8, len(self.electrodes))
        self.assertEqual(0, self.electrodes[0]['shank_id'])
        self.assertEqual(1, self.electrodes[5]['shank_id'])
        self.assertEqual(0, self.electrodes[0]['id'])
        self.assertEqual(1, self.electrodes[1]['id'])
        self.assertEqual(3, self.electrodes[0]['electrode_group'])
        self.assertEqual(3, self.electrodes[5]['electrode_group'])
