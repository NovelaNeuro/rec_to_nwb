import os
from unittest import TestCase

from src.datamigration.nwb.components.task.task_builder import TaskBuilder

path = os.path.dirname(os.path.abspath(__file__))


class TestTaskBuilder(TestCase):

    def test_should_build_task(self):
        metadata = {"tasks": [{"task_name": "Sleep", "task_description": "The animal sleeps in a small empty box."}]}
        task_builder = TaskBuilder(metadata)

        dynamic_table_with_tasks = task_builder.build()

        self.assertIsNotNone(dynamic_table_with_tasks)
        self.assertEqual('task_name', dynamic_table_with_tasks.columns[0].name)
        self.assertEqual(['Sleep'], dynamic_table_with_tasks.columns[0].data)
        self.assertEqual('task_description', dynamic_table_with_tasks.columns[1].name)
        self.assertEqual(['The animal sleeps in a small empty box.'], dynamic_table_with_tasks.columns[1].data)

    def test_no_table_when_no_metadata(self):
        task_builder = TaskBuilder(None)

        none_dynamic_table = task_builder.build()

        self.assertIsNone(none_dynamic_table)

    def test_no_table_when_tasks_do_not_exist(self):
        metadata = {"tasks": None}
        task_builder = TaskBuilder(metadata)

        none_dynamic_table = task_builder.build()

        self.assertIsNone(none_dynamic_table)

    def test_no_table_when_tasks_are_empty_list(self):
        metadata = {"tasks": []}
        task_builder = TaskBuilder(metadata)

        none_dynamic_table = task_builder.build()

        self.assertIsNone(none_dynamic_table)
