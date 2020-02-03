import logging.config
import os
import unittest
from pathlib import Path

from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata
from src.datamigration.nwb_file_builder import NWBFileBuilder

path = Path(__file__).parent.parent
path.resolve()

logging.config.fileConfig(fname=str(path) + '/../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@unittest.skip("NWB file creation")
class TestNwbFullGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        metadata = NWBMetadata(str(path) + '/datamigration/res/metadata.yml',
                               [str(path) + '/datamigration/res/probe1.yml',
                                str(path) + '/datamigration/res/probe2.yml',
                                str(path) + '/datamigration/res/probe3.yml'])
        cls.nwb_builder = NWBFileBuilder(
            data_path=str(path) + '/test_data/',
            animal_name='beans',
            date='20190718',
            nwb_metadata=metadata,
            process_dio=False,
            process_mda=True
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
