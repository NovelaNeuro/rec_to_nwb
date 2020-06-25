import os
import unittest

from rec_to_nwb.processing.nwb.components.iterator.multi_thread_data_iterator import MultiThreadDataIterator
from rec_to_nwb.processing.nwb.components.position.fl_position_manager import FlPositionManager
from rec_to_nwb.processing.nwb.components.position.position_creator import PositionCreator
from rec_to_nwb.processing.tools.dataset import Dataset

path = os.path.dirname(os.path.abspath(__file__))


@unittest.skip("test requires continuoustime.dat file and can't be used on travis")
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
        position = [
            position_creator.create(fl_position)
            for fl_position in fl_positions
        ]

        self.assertIsInstance(position, list)
        self.assertEqual(position[0].spatial_series['series'].conversion, 0.02)
        self.assertIsInstance(position[0].spatial_series['series'].data, MultiThreadDataIterator)
        self.assertEqual(position[0].spatial_series['series'].data.shape, [32658, 4])
        self.assertEqual(position[0].spatial_series['series'].timestamps_unit, 'seconds')
        self.assertEqual(position[0].spatial_series['series'].unit, 'meters')
