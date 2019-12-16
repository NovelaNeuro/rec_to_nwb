import os
import unittest
from pathlib import Path

from src.datamigration.nwb_file_builder import NWBFileBuilder

path = Path(__file__).parents[1]


#@unittest.skip("NWB file creation")
class TestNwbFullGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nwbBuilder = NWBFileBuilder(
            data_path=path.name + '/testdata',
            animal_name='beans',
            date='20190718',
            dataset='01_s1',
            metadata_path='datamigration/res/metadata.yml',
            header_path='datamigration/res/fl_lab_sample_header.xml'
        )

    def test_generate_nwb(self):
        content = self.nwbBuilder.build()
        self.nwbBuilder.write(content)
        self.assertIsNotNone(self.nwbBuilder)

    @classmethod
    def tearDownClass(cls):
        del cls.nwbBuilder
        if os.path.isfile('output.nwb'):
            os.remove('output.nwb')