import os
import unittest

from src.datamigration.nwb_file_builder import NWBFileBuilder
from .experiment_data import ExperimentData


@unittest.skip("NWB file creation")
class TestNwbFullGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nwbBuilder = NWBFileBuilder(
            data_path=ExperimentData.root_path,
            animal_name='beans',
            date='20190718',
            dataset='01_s1',
            config_path='datamigration/res/metadata.yml',
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