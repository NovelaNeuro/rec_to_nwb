import unittest

from pynwb import NWBHDF5IO

from src.test.e2etests.experiment_data import ExperimentData


class TestMDAMigration(unittest.TestCase):

    def setUp(self):
        self.builder = NWBFileBuilder(ExperimentData.root_path, 'beans', '20190718', '01_s1')

    @unittest.skip("DOES NOT WORK!!!")
    def test_reading_mda(self):
        self.builder.build()
        self.assertIsNotNone(1)
        with NWBHDF5IO(path='mda_test.nwb', mode='r') as io:
            nwb_file = io.read()
            print(nwb_file)