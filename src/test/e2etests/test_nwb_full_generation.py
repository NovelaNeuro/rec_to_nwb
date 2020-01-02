import os
import unittest
from pathlib import Path

from src.datamigration.nwb_file_builder import NWBFileBuilder

path = Path(__file__).parent.parent
path.resolve()


# @unittest.skip("NWB file creation")
class TestNwbFullGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.nwbBuilder = NWBFileBuilder(
            data_path=str(path) + '/test_data/',
            animal_name='beans',
            date='20190718',
            metadata_path=str(path) + '/datamigration/res/metadata.yml',
            probes_path=str(path) + '/datamigration/res/'
           )

    @unittest.skip("NWB file creation")
    def test_generate_nwb(self):
        content = self.nwbBuilder.build()
        self.nwbBuilder.write(content)
        self.assertIsNotNone(self.nwbBuilder)

    @classmethod
    def tearDownClass(cls):
        del cls.nwbBuilder
        if os.path.isfile('output.nwb'):
            os.remove('output.nwb')