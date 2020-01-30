import os
import unittest

from src.datamigration.nwb_builder.builders.pos_builder import PosBuilder
from src.datamigration.tools.file_scanner import Dataset
from src.datamigration.nwb_builder.extractors.pos_extractor import POSExtractor

path = os.path.dirname(os.path.abspath(__file__))


@unittest.skip("test requires continuoustime.dat file and can't be used on travis")
class TestPOSExtraction(unittest.TestCase):

    def setUp(self):
        self.dataset = self.create_test_dataset()
        self.pos_extractor = POSExtractor(datasets=[self.dataset])
        self.position = self.pos_extractor.get_position()
        self.timestamps = self.pos_extractor.get_timestamps()

    @staticmethod
    def create_test_dataset():
        dataset = Dataset('test_dataset')
        dataset.add_data_to_dataset(path + '/../datamigration/res/pos_test/', 'pos')
        dataset.add_data_to_dataset(path + '/../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.time/',
                                    'time')
        return dataset

    def test_reading_pos_extractor(self):
        pos_data = PosBuilder.build(self.position, self.timestamps)
        self.assertIsNotNone(pos_data)
        self.assertEqual([32658, 4], pos_data['Fields'].data.shape,
                         'Shape should be [32658, 4]')
        self.assertEqual((32658,), pos_data['Fields'].timestamps.shape,
                         'Shape should be (32658,)')
