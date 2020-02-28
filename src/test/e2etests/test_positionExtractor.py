import os
import unittest

from testfixtures import should_raise

from src.datamigration.exceptions.none_param_in_init_exception import NoneParamInInitException
from src.datamigration.nwb.components.position.lf_position_manager import LfPositionManager
from src.datamigration.nwb.components.position.position_creator import PositionCreator
from src.datamigration.tools.file_scanner import Dataset

path = os.path.dirname(os.path.abspath(__file__))


@unittest.skip("test requires continuoustime.dat file and can't be used on travis")
class TestPositionExtraction(unittest.TestCase):

    @staticmethod
    def create_test_dataset():
        dataset = Dataset('test_dataset')
        dataset.add_data_to_dataset(path + '/../datamigration/res/pos_test/', 'pos')
        dataset.add_data_to_dataset(path + '/../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.time/',
                                    'time')
        return dataset

    def test_position_extractor_reading_data_successfully(self):
        dataset = self.create_test_dataset()

        lf_position_manager = LfPositionManager(datasets=[dataset, ])
        position_creator = PositionCreator()

        lf_position = lf_position_manager.get_lf_position()
        position = position_creator.create(lf_position)

        self.assertIsNotNone(position)
        self.assertEqual([32658, 4], position['Fields'].data.shape,
                         'Shape should be [32658, 4]')
        self.assertEqual((32658,), position['Fields'].timestamps.shape,
                         'Shape should be (32658,)')

    @should_raise(NoneParamInInitException)
    def test_position_extractor_fails_reading_data_due_to_None_datasets(self):
        lf_position_manager = LfPositionManager(datasets=None)
        position_creator = PositionCreator()

        lf_position = lf_position_manager.get_lf_position()
        position_creator.create(lf_position)
