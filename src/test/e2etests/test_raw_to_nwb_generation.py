import logging.config
import os
import unittest
from pathlib import Path

from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata
from src.datamigration.raw_to_nwb_builder import RawToNWBBuilder

path = Path(__file__).parent.parent
path.resolve()

logging.config.fileConfig(fname=str(path) + '/../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@unittest.skip("Super heavy RAW to NWB Generation")
class TestRawToNWBGeneration(unittest.TestCase):

    def setUp(self):
        metadata = NWBMetadata(str(path) + '/datamigration/res/metadata.yml',
                               [str(path) + '/datamigration/res/probe1.yml',
                                str(path) + '/datamigration/res/probe2.yml',
                                str(path) + '/datamigration/res/probe3.yml'])
        self.builder = RawToNWBBuilder(animal_name='beans',
                                       data_path=str(path) + '/test_data/',
                                       dates=['20190718'],
                                       nwb_metadata=metadata,
                                       output_path='',
                                       extract_spikes=False,
                                       extract_mda=True,
                                       extract_time=True,
                                       extract_lfps=False,
                                       extract_analog=False,
                                       extract_dio=True,
                                       )

    def test_from_raw_to_nwb_generation(self):
        self.builder.build_nwb()
        self.assertTrue(os.path.exists('beans20190718.nwb'), 'NWBFile did not build')

    def tearDown(self):
        self.builder.cleanup()
