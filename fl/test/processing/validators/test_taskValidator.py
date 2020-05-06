from unittest import TestCase

from testfixtures import should_raise

from fl.processing.exceptions.invalid_metadata_exception import InvalidMetadataException
from fl.processing.validation.task_validator import TaskValidator


class TestTaskValidator(TestCase):

    def test_task_validator_existing_tasks_valid(self):
        tasks = [{'task_name': 'task1'}, {'task_name': 'task2'}]
        task_validator = TaskValidator(tasks)
        result = task_validator.create_summary()
        self.assertTrue(result.is_valid())

    @should_raise(InvalidMetadataException)
    def test_task_validator_empty_tasks_failed(self):
        tasks = []
        task_validator = TaskValidator(tasks)
        result = task_validator.create_summary()
        self.assertFalse(result.is_valid())


