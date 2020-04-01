import os
import unittest
from pathlib import Path

from fl.datamigration.nwb_file_builder import NWBFileBuilder

path = Path(__file__).parent.parent
path.resolve()


@unittest.skip("NWB file creation")
class TestNwbFullGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        metadata = {'metadata': str(path) + '/datamigration/res/metadata.yml',
                    'probes': [str(path) + '/datamigration/res/probe1.yml',
                               str(path) + '/datamigration/res/probe2.yml',
                               str(path) + '/datamigration/res/probe3.yml']}
        cls.nwb_builder = NWBFileBuilder(
            data_path=str(path) + '/test_data/',
            animal_name='beans',
            date='20190718',
            nwb_metadata_paths=metadata,
            process_dio=False,
            process_mda=False,
            process_analog=False
        )

    def test_generate_nwb(self):
        content = self.nwb_builder.build()
        self.nwb_builder.write(content)
        self.assertIsNotNone(self.nwb_builder)

    @classmethod
    def tearDownClass(cls):
        del cls.nwb_builder
        if os.path.isfile('output.nwb'):
            os.remove('output.nwb')
