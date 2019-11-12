import unittest

from pynwb import NWBHDF5IO

from src.datamigration.nwb_file_builder import NWBFileBuilder
from .experiment_data import ExperimentData


class TestNWBBuilder(unittest.TestCase):

    def setUp(self):
        self.nwbBuilder = NWBFileBuilder(
            pos_path=ExperimentData.pos_path + ExperimentData.pos_file,
            metadata_path=ExperimentData.metadata_path,
            mda_path=ExperimentData.mda_path,
            mda_timestamp_name=ExperimentData.mda_timestamp,
            xml_path=ExperimentData.xml_path,
            output_file_path='output.nwb'
        )

    # @unittest.skip("Super heavy NWB generation")
    def test_run_nwb_generation_from_preprocessed_data(self):
        nwb_file_path = self.nwbBuilder.build()
        with NWBHDF5IO(path=nwb_file_path, mode='r') as io:
            nwb_file = io.read()
            print(nwb_file)
            print('Details: ')
            print('Position: ' + str(nwb_file.processing['position'].data_interfaces['Position']))
            print('Task: ' + str(nwb_file.processing['task'].data_interfaces['novela task']))
            print('Apparatus: ' + str(nwb_file.processing['apparatus'].data_interfaces['apparatus']))
