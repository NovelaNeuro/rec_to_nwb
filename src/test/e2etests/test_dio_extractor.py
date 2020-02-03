import logging.config
import unittest
from pathlib import Path

from pynwb.behavior import BehavioralEvents

from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata

path = Path(__file__).parent.parent
path.resolve()

logging.config.fileConfig(fname=str(path) + '/../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@unittest.skip('DIO test require real dio files')
class TestDio(unittest.TestCase):
    def setUp(self):
        self.dio_data = DioExtractor(data_path=str(path) + '/test_data/beans/preprocessing/20190718/',
                                     metadata=NWBMetadata(metadata_path=str(path) + '/datamigration/res/metadata.yml',
                                                          probes_paths=[]).metadata)

    def test_dio_extractor(self):
        self.assertIsNotNone(self.dio_data)
        self.assertIsInstance(self.dio_data.get_dio(), BehavioralEvents)
