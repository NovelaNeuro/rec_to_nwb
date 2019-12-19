import unittest
from pathlib import Path

from src.datamigration.nwb_builder.dio_extractor import DioExtractor

path = Path(__file__).parent.parent
path.resolve()


@unittest.skip('DIO test require real dio files')
class TestDio(unittest.TestCase):

    def setUp(self):
        self.dio_data = DioExtractor(data_path=str(path) + '/test_data/beans/preprocessing/20190718/',
                                     metadata_path=str(path) + '/res/metadata.yml').get_dio()

    def test_dio_extractor(self):
        self.assertIsNotNone(self.dio_data)
        self.assertNotEqual([], self.dio_data.fields['time_series']['Din3'].data)

