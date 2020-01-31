import os
import unittest

from src.datamigration.nwb_builder.builders.position_builder import PositionBuilder
from src.datamigration.tools.file_scanner import Dataset

path = os.path.dirname(os.path.abspath(__file__))


@unittest.skip("test requires continuoustime.dat file and can't be used on travis")
class TestPositionExtraction(unittest.TestCase):

    def setUp(self):
        self.dataset = self.create_test_dataset()
        self.pos_builder = PositionBuilder(datasets=[self.dataset,])
        self.pos_extractor = self.pos_builder.position_extractor
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
        pos_data = self.pos_builder.build()
        self.assertIsNotNone(pos_data)
        self.assertEqual([32658, 4], pos_data['Fields'].data.shape,
                         'Shape should be [32658, 4]')
        self.assertEqual((32658,), pos_data['Fields'].timestamps.shape,
                         'Shape should be (32658,)')
