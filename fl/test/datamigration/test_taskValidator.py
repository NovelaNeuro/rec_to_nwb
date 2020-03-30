from unittest import TestCase
from unittest.mock import Mock

from fl.datamigration.tools.dataset import Dataset
from fl.datamigration.tools.task_validator import TaskValidator


class TestTaskValidator(TestCase):

    def setUp(self):
        dataset_1_mock = Mock(spec=Dataset)
        dataset_1_mock.name = 'mock1'
        dataset_2_mock = Mock(spec=Dataset)
        dataset_2_mock.name = 'mock2'
        self.datasets = [dataset_1_mock, dataset_2_mock]

    def test_task_validator_equal_number_of_task_and_epochs_valid(self):
        tasks = [{'task_name': 'task1'}, {'task_name': 'task2'}]
        task_validator = TaskValidator(self.datasets, tasks)
        self.assertTrue(task_validator.is_number_of_tasks_valid())

    def test_task_validator_different_number_of_tasks_and_epochs_failed(self):
        tasks = [{'task_name': 'task1'}, {'task_name': 'task2'}, {'task_name': 'task3'}]
        task_validator = TaskValidator(self.datasets, tasks)
        self.assertFalse(task_validator.is_number_of_tasks_valid())


