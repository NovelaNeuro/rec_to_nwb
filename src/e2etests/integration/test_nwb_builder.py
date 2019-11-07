import unittest
from pynwb import NWBHDF5IO
from src.datamigration.nwb_file_builder import NWBFileCreator


class TestNWBBuilder(unittest.TestCase):

    def setUp(self):
        with NWBHDF5IO(NWBFileCreator().build(), mode='r') as io:
            self.nwb_file = io.read()

    def test_metadata(self):
        self.assertEqual('hulk', self.nwb_file.experimenter)

    def test_pos(self):
        pass

    def test_mda(self):
        pass

