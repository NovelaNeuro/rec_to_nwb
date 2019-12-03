import unittest

from src.datamigration.nwb_builder.dio_extractor import DioExtractor


class TestDio(unittest.TestCase):

    def setUp(self):
        self.dio_data = DioExtractor('C:/Users/wmery/PycharmProjects/LorenFranksDataMigration/src/test/test_data/jaq/preprocessing/20190911/20190911_jaq_01_s1.DIO').get_dio()

    def test_dio_extractor(self):
        self.assertIsNotNone(self.dio_data)
        self.assertNotEqual([], self.dio_data['time_series'].data)
