from unittest import TestCase

from rec_to_nwb.processing.nwb.components.position.fl_position import FlPosition
from rec_to_nwb.processing.nwb.components.position.fl_position_manager import FlPositionManager


class MockFlPositionExtractor:

    @staticmethod
    def get_positions():
        return ['1', '2']

    @staticmethod
    def get_columns_labels():
        return ['a', 'b']

    @staticmethod
    def get_timestamps():
        return [111, 222]


class TestPositionManager(TestCase):

    def test_position_manager_get_fl_position_successfully(self):
        mock_dataset = []
        mock_metadata = {
            'cameras': [
                {'id': '0', 'meters_per_pixel': '0.02'},
                {'id': '1', 'meters_per_pixel': '0.03'},
                {'id': '2', 'meters_per_pixel': '0.5'},
            ],
            'tasks': [
                {"task_name": "Sleep", "task_description": "The animal sleeps in a small empty box.",
                 'camera_id': ['0'], 'task_epochs': ['1', '3', '5']},
                {"task_name": "Stem+Leaf", "task_description": "Spatial Bandit",
                 'camera_id': ['2'], 'task_epochs': ['2', '4']},
            ]
        }
        mock_dataset_names = ['01_s1', '02_s1']

        fl_position_manager = FlPositionManager(
            datasets=mock_dataset,
            metadata=mock_metadata,
            dataset_names=mock_dataset_names,
        )
        fl_position_manager.fl_position_extractor = MockFlPositionExtractor()
        fl_positions = fl_position_manager.get_fl_positions()

        self.assertIsInstance(fl_positions, list)
        self.assertEqual(len(fl_positions), 2)
        self.assertIsInstance(fl_positions[0], FlPosition)
        self.assertIsInstance(fl_positions[1], FlPosition)
        self.assertEqual(fl_positions[0].position_data, '1')
        self.assertEqual(fl_positions[0].column_labels, 'a')
        self.assertEqual(fl_positions[0].timestamps, 111)
        self.assertEqual(fl_positions[0].conversion, 0.02)
        self.assertEqual(fl_positions[1].position_data, '2')
        self.assertEqual(fl_positions[1].column_labels, 'b')
        self.assertEqual(fl_positions[1].timestamps, 222)
        self.assertEqual(fl_positions[1].conversion, 0.5)
