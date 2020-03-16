import os
import unittest

from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.position.fl_position_manager import FlPositionManager
from fl.datamigration.nwb.components.position.position_creator import PositionCreator
from fl.datamigration.tools.dataset import Dataset

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

        fl_position_manager = FlPositionManager(datasets=[dataset, ])
        position_creator = PositionCreator()

        fl_position = fl_position_manager.get_fl_position()
        position = position_creator.create(fl_position)

        self.assertIsNotNone(position)
        self.assertEqual([32658, 4], position['Fields'].data.shape,
                         'Shape should be [32658, 4]')
        self.assertEqual((32658,), position['Fields'].timestamps.shape,
                         'Shape should be (32658,)')

    @should_raise(NoneParamException)
    def test_position_extractor_fails_reading_data_due_to_None_datasets(self):
        fl_position_manager = FlPositionManager(datasets=None)
        position_creator = PositionCreator()

        fl_position = fl_position_manager.get_fl_position()
        position_creator.create(fl_position)
