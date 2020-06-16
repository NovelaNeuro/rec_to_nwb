import os
from datetime import datetime
from unittest import TestCase

from dateutil.tz import tzlocal
from pynwb import NWBFile, ProcessingModule, NWBHDF5IO

from rec_to_nwb.processing.nwb.components.task.task_builder import TaskBuilder

path = os.path.dirname(os.path.abspath(__file__))


class TestTaskBuilder(TestCase):

    def test_task_builder_build_task_successfully(self):
        metadata = {"tasks": [
            {"task_name": "Sleep", "task_description": "The animal sleeps in a small empty box.",
             'camera_id': [0], 'task_epochs': [1, 3, 5]},
            {"task_name": "Stem+Leaf", "task_description": "Spatial Bandit",
             'camera_id': [1, 2], 'task_epochs': [2, 4]},
        ]}
        task_builder = TaskBuilder(metadata)

        dynamic_table_with_tasks = task_builder.build()

        self.assertIsNotNone(dynamic_table_with_tasks)
        self.assertEqual('task_name_index', dynamic_table_with_tasks.columns[0].name)
        self.assertEqual([0, 1], dynamic_table_with_tasks.columns[0].data)
        self.assertEqual('task_name', dynamic_table_with_tasks.columns[1].name)
        self.assertEqual(['Sleep', 'Stem+Leaf'], dynamic_table_with_tasks.columns[1].data)
        self.assertEqual('task_description_index', dynamic_table_with_tasks.columns[2].name)
        self.assertEqual([0, 1], dynamic_table_with_tasks.columns[2].data)
        self.assertEqual('task_description', dynamic_table_with_tasks.columns[3].name)
        self.assertEqual(['The animal sleeps in a small empty box.', 'Spatial Bandit'],
                         dynamic_table_with_tasks.columns[3].data)
        self.assertEqual('camera_id_index', dynamic_table_with_tasks.columns[4].name)
        self.assertEqual([0, 1], dynamic_table_with_tasks.columns[4].data)
        self.assertEqual('camera_id', dynamic_table_with_tasks.columns[5].name)
        self.assertEqual([[0], [1, 2]], dynamic_table_with_tasks.columns[5].data)
        self.assertEqual('task_epochs_index', dynamic_table_with_tasks.columns[6].name)
        self.assertEqual([0, 1], dynamic_table_with_tasks.columns[6].data)
        self.assertEqual('task_epochs', dynamic_table_with_tasks.columns[7].name)
        self.assertEqual([[1, 3, 5], [2, 4]], dynamic_table_with_tasks.columns[7].data)

    def test_task_builder_build_task_and_write_to_nwb_successfully(self):
        nwb_content = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )
        processing_module = ProcessingModule('pm', 'none')
        metadata = {"tasks": [
            {"task_name": "Sleep", "task_description": "The animal sleeps in a small empty box.",
             'camera_id': [0], 'task_epochs': [1, 3, 5]},
            {"task_name": "Stem+Leaf", "task_description": "Spatial Bandit",
             'camera_id': [1, 2], 'task_epochs': [2, 4]},
        ]}

        task_builder = TaskBuilder(metadata)
        task = task_builder.build()
        processing_module.add(task)
        nwb_content.add_processing_module(processing_module)

        with NWBHDF5IO(path='task.nwb', mode='w') as nwb_file_io:
            nwb_file_io.write(nwb_content)
            nwb_file_io.close()

        with NWBHDF5IO(path='task.nwb', mode='r') as nwb_file_io:
            nwb_content = nwb_file_io.read()
            print(nwb_content.processing['pm'].data_interfaces['task'])

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
