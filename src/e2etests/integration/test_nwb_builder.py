import unittest

from pynwb import NWBHDF5IO

from src.datamigration.nwb_file_builder import NWBFileCreator
from src.e2etests.integration.experiment_data import ExperimentData


class TestNWBBuilder(unittest.TestCase):

    def setUp(self):
        self.nwbCreator = NWBFileCreator(
            pos_path=ExperimentData.pos_path + ExperimentData.pos_file,
            metadata_path=ExperimentData.metadata_path,
            mda_path=ExperimentData.mda_path,
            mda_timestamp_name=ExperimentData.mda_timestamp,
            output_file_path='output.nwb'
        )

    def test_run_nwb_generation_from_preprocessed_data(self):
        with NWBHDF5IO(self.nwbCreator.build(), mode='r') as io:
            nwb_file = io.read()
            print(nwb_file)
