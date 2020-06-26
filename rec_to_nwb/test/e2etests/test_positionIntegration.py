import os
import unittest

from pynwb.behavior import Position

from rec_to_nwb.processing.nwb.components.iterator.multi_thread_data_iterator import MultiThreadDataIterator
from rec_to_nwb.processing.nwb.components.position.fl_position_manager import FlPositionManager
from rec_to_nwb.processing.nwb.components.position.position_creator import PositionCreator
from rec_to_nwb.processing.tools.dataset import Dataset

path = os.path.dirname(os.path.abspath(__file__))


# @unittest.skip("test requires continuoustime.dat file and can't be used on travis")
class TestPositionIntegration(unittest.TestCase):

    @staticmethod
    def create_test_dataset():
        dataset = Dataset('test_dataset')
        dataset.add_data_to_dataset(path + '/../processing/res/pos_test/', 'pos')
        dataset.add_data_to_dataset(path + '/../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.time/',
                                    'time')
        return dataset

    def test_position_extractor_reading_data_successfully(self):
        dataset = self.create_test_dataset()

        fl_position_manager = FlPositionManager(
            datasets=[dataset],
            metadata={
                'cameras': [
                    {'id': '0', 'meters_per_pixel': '0.02'},
                    {'id': '1', 'meters_per_pixel': '0.03'},
                    {'id': '2', 'meters_per_pixel': '0.5'},
                ],
                'tasks': [
                    {"task_name": "Sleep", "task_description": "The animal sleeps in a small empty box.",
                     'camera_id': ['0'], 'task_epochs': ['1', '3', '5']}
                ]
            },
            dataset_names=['01_s1']
        )
        position_creator = PositionCreator()
        fl_positions = fl_position_manager.get_fl_positions()
        positions = position_creator.create_all(fl_positions)

        self.assertIsInstance(positions, Position)
        self.assertEqual(positions.spatial_series['series_0'].conversion, 0.02)
        self.assertIsInstance(positions.spatial_series['series_0'].data, MultiThreadDataIterator)
        self.assertEqual(positions.spatial_series['series_0'].data.shape, [32658, 4])
        self.assertEqual(positions.spatial_series['series_0'].timestamps_unit, 'seconds')
        self.assertEqual(positions.spatial_series['series_0'].unit, 'meters')
