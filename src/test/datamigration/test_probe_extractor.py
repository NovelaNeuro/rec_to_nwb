import unittest
import os

from src.datamigration.nwb_builder.probe_extractor import ProbeExtractor

path = os.path.dirname(os.path.abspath(__file__))


class TestProbeExtractor(unittest.TestCase):

    def setUp(self):
        self.probes = [ProbeExtractor(probe_name) for probe_name
                  in [path+'/res/probe.yml', path+'/res/probe2.yml', path+'/res/probe3.yml']
                  ]

    def test_probes(self):
        self.assertEqual(3, len(self.probes))
        self.assertEqual('tetrode_12.5', self.probes[0].probe_type)
        self.assertEqual(32, len(self.probes[1].shanks))