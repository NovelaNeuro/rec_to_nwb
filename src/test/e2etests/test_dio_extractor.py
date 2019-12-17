import unittest
import src.datamigration.file_scanner as fs
from src.datamigration.nwb_builder.dio_extractor import DioExtractor


@unittest.skip('DIO test require real dio files')
class TestDio(unittest.TestCase):

    def setUp(self):
        self.dio_data = DioExtractor(fs.DataScanner('test_data/').data['beans']['20190718']
                                     ['01_s1'].get_data_path_from_dataset('DIO')).get_dio()
    def test_dio_extractor(self):
        self.assertIsNotNone(self.dio_data)
        self.assertNotEqual([], self.dio_data.time_series)
        self.assertNotEqual([], self.dio_data.time_series['behavioral timeseries in'].data)

