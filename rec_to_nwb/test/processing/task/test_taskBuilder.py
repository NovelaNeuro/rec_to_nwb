import os
from unittest import TestCase

from rec_to_nwb.processing.nwb.components.task.task_builder import TaskBuilder

path = os.path.dirname(os.path.abspath(__file__))


class TestTaskBuilder(TestCase):

    def test_task_builder_build_task_successfully(self):
        metadata = {"tasks": [
            {"task_name": "Sleep", "task_description": "The animal sleeps in a small empty box.",
             'camera_id': [1, 2], 'task_epochs': [1, 3]}
        ]}
        task_builder = TaskBuilder(metadata)

        dynamic_table_with_tasks = task_builder.build()

        self.assertIsNotNone(dynamic_table_with_tasks)
        self.assertEqual('task_name_index', dynamic_table_with_tasks.columns[0].name)
        self.assertEqual([0], dynamic_table_with_tasks.columns[0].data)
        self.assertEqual('task_name', dynamic_table_with_tasks.columns[1].name)
        self.assertEqual(['Sleep'], dynamic_table_with_tasks.columns[1].data)
        self.assertEqual('task_description_index', dynamic_table_with_tasks.columns[2].name)
        self.assertEqual([0], dynamic_table_with_tasks.columns[2].data)
        self.assertEqual('task_description', dynamic_table_with_tasks.columns[3].name)
        self.assertEqual(['The animal sleeps in a small empty box.'], dynamic_table_with_tasks.columns[3].data)
        self.assertEqual('camera_id_index', dynamic_table_with_tasks.columns[4].name)
        self.assertEqual([0], dynamic_table_with_tasks.columns[4].data)
        self.assertEqual('camera_id', dynamic_table_with_tasks.columns[5].name)
        self.assertEqual([[1, 2]], dynamic_table_with_tasks.columns[5].data)
        self.assertEqual('task_epochs_index', dynamic_table_with_tasks.columns[6].name)
        self.assertEqual([0], dynamic_table_with_tasks.columns[6].data)
        self.assertEqual('task_epochs', dynamic_table_with_tasks.columns[7].name)
        self.assertEqual([[1, 3]], dynamic_table_with_tasks.columns[7].data)

    def test_task_builder_build_empty_table_when_no_metadata(self):
        task_builder = TaskBuilder(None)

        none_dynamic_table = task_builder.build()

        self.assertIsNone(none_dynamic_table)

    def test_task_builder_build_empty_table_when_tasks_do_not_exist(self):
        metadata = {"tasks": None}
        task_builder = TaskBuilder(metadata)

        none_dynamic_table = task_builder.build()

        self.assertIsNone(none_dynamic_table)

    def test_task_builder_build_empty_table_when_tasks_are_empty_list(self):
        metadata = {"tasks": []}
        task_builder = TaskBuilder(metadata)

        none_dynamic_table = task_builder.build()

        self.assertIsNone(none_dynamic_table)
