import os
import unittest
from pathlib import Path

from src.datamigration.raw_to_nwb_builder import RawToNWBBuilder

path = Path(__file__).parent.parent
path.resolve()


# @unittest.skip("Super heavy RAW to NWB Generation")
class TestRawToNWBGeneration(unittest.TestCase):

    def setUp(self):
        self.builder = RawToNWBBuilder(animal_name='beans',
                                       data_path=str(path) + '/test_data/',
                                       date='20190718',
                                       dataset='01_s1',
                                       metadata_path=str(path) + '/res/metadata.yml',
                                       output_path='raw2nwb_output.nwb'
                                       )

    def test_from_raw_to_nwb_generation(self):
        self.builder.build_nwb()
        self.assertTrue(os.path.exists('raw2nwb_output.nwb'), 'NWBFile did not build')

    def test_empty_trash(self):
        self.builder.cleanup()
        self.assertTrue(os.path.exists('raw2nwb_output.nwb'), 'NWBFile did not build')

    # def tearDown(self):
    #     self.builder.cleanup()
