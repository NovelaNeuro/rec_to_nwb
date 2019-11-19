import unittest

from pynwb import NWBHDF5IO

from src.datamigration.file_scanner import DataScanner
from src.datamigration.nwb_file_builder import NWBFileBuilder
from .experiment_data import ExperimentData


class TestNWBBuilder(unittest.TestCase):

    def setUp(self):
        self.data_scanner = DataScanner(ExperimentData.root_path)
        animal = self.data_scanner.get_all_animals()[0]
        date = self.data_scanner.get_all_experiment_dates(animal)[0]
        dataset = self.data_scanner.get_all_datasets(animal, date)[0]
        self.nwbBuilder = NWBFileBuilder(
            data_path=ExperimentData.root_path,
            animal_name=animal,
            date=date,
            dataset=dataset,
            output_file_location='',
            output_file_name='output.nwb'
        )

    @unittest.skip("Super heavy NWB generation")
    def test_run_nwb_generation_from_preprocessed_data(self):
        nwb_file_path = self.nwbBuilder.build(mda_data_chunk_size=4)
        with NWBHDF5IO(path=nwb_file_path, mode='r') as io:
            nwb_file = io.read()
            print(nwb_file)
            print('Details: ')
            print('Position: ' + str(nwb_file.processing['position'].data_interfaces['Position']))
            print('Task: ' + str(nwb_file.processing['task'].data_interfaces['novela task']))
            print('Apparatus: ' + str(nwb_file.processing['apparatus'].data_interfaces['apparatus']))
