from unittest import TestCase

from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.invalid_metadata_exception import InvalidMetadataException
from rec_to_nwb.processing.exceptions.not_equal_param_length_exception import NotEqualParamLengthException
from rec_to_nwb.processing.nwb.components.position.fl_position import FlPosition
from rec_to_nwb.processing.nwb.components.position.fl_position_manager import FlPositionManager


class MockFlPositionExtractor:

    @staticmethod
    def get_positions():
        # In the real project, we get list of MultiThreadDataIterator objects
        return ['1', '2']

    @staticmethod
    def get_columns_labels():
        return ['a', 'b']

    @staticmethod
    def get_timestamps():
        # In the real project, we get list of MultiThreadTimestampIterator objects
        return [111, 222]


class MockBadFlPositionExtractor:

    @staticmethod
    def get_positions():
        # In the real project, we get list of MultiThreadDataIterator objects
        return ['1']

    @staticmethod
    def get_columns_labels():
        return ['a', 'b']

    @staticmethod
    def get_timestamps():
        # In the real project, we get list of MultiThreadTimestampIterator objects
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
            process_timestamps=True
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

    @should_raise(TypeError)
    def test_position_manager_failed_due_to_none_param(self):
        FlPositionManager(
            datasets=None,
            metadata=None,
            dataset_names=None,
            process_timestamps=True
        )

    @should_raise(InvalidMetadataException)
    def test_position_manager_failed_due_to_metadata_without_task_epochs_for_dataset(self):
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
        mock_dataset_names = ['01_s1', '02_s1', '08_s1']

        fl_position_manager = FlPositionManager(
            datasets=mock_dataset,
            metadata=mock_metadata,
            dataset_names=mock_dataset_names,
            process_timestamps=True
        )
        fl_position_manager.fl_position_extractor = MockFlPositionExtractor()
        fl_position_manager.get_fl_positions()

    @should_raise(NotEqualParamLengthException)
    def test_position_manager_failed_due_to_not_equal_data_length(self):
        mock_dataset = []
        mock_metadata = {
            'cameras': [
                {'id': '0', 'meters_per_pixel': '0.02'},
                {'id': '1', 'meters_per_pixel': '0.03'},
                {'id': '2', 'meters_per_pixel': '0.03'},
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
            process_timestamps=True
        )
        fl_position_manager.fl_position_extractor = MockBadFlPositionExtractor()
        fl_position_manager.get_fl_positions()
