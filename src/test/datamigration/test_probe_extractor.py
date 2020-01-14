
import os
import unittest

from src.datamigration.nwb_builder.probe_extractor import ProbesExtractor

path = os.path.dirname(os.path.abspath(__file__))


class TestProbeExtractor(unittest.TestCase):

    def setUp(self):
        self.probes = ProbesExtractor([path + '/res/probe1.yml',
                                       path + '/res/probe2.yml',
                                       path + '/res/probe3.yml'])

    def test_probes(self):
        self.assertEqual(3, len(self.probes.probes_content))
        self.assertEqual('tetrode_12.5', self.probes.probes_content[0]['probe_type'])