import os

from pynwb.testing import TestCase
from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.none_param_exception import NoneParamException
from rec_to_nwb.processing.nwb.components.task.fl_task import FlTask
from rec_to_nwb.processing.nwb.components.task.task_manager import TaskManager

path = os.path.dirname(os.path.abspath(__file__))


class TestTaskManager(TestCase):

    def test_task_manager_get_fl_tasks_successfully(self):
        metadata = {"tasks": [
            {"task_name": "Sleep", "task_description": "The animal sleeps in a small empty box.",
             'camera_id': [0], 'task_epochs': [1, 3, 5]},
            {"task_name": "Stem+Leaf", "task_description": "Spatial Bandit",
             'camera_id': [1, 2], 'task_epochs': [2, 4]},
        ]}
        task_manager = TaskManager(metadata)

        fl_tasks = task_manager.get_fl_tasks()

        self.assertIsInstance(fl_tasks, list)
        self.assertIsInstance(fl_tasks[0], FlTask)
        self.assertIsInstance(fl_tasks[1], FlTask)

        self.assertEqual(fl_tasks[0].name, 'task_0')
        self.assertEqual(fl_tasks[0].description, '')
        self.assertEqual(fl_tasks[0].columns[0].name, 'task_name')
        self.assertEqual(fl_tasks[0].columns[0].data, ['Sleep'])
        self.assertEqual(fl_tasks[0].columns[1].name, 'task_description')
        self.assertEqual(fl_tasks[0].columns[1].data, ['The animal sleeps in a small empty box.'])
        self.assertEqual(fl_tasks[0].columns[2].name, 'camera_id')
        self.assertEqual(fl_tasks[0].columns[2].data, [[0]])
        self.assertEqual(fl_tasks[0].columns[3].name, 'task_epochs')
        self.assertEqual(fl_tasks[0].columns[3].data, [[1, 3, 5]])

        self.assertEqual(fl_tasks[1].name, 'task_1')
        self.assertEqual(fl_tasks[1].description, '')
        self.assertEqual(fl_tasks[1].columns[0].name, 'task_name')
        self.assertEqual(fl_tasks[1].columns[0].data, ['Stem+Leaf'])
        self.assertEqual(fl_tasks[1].columns[1].name, 'task_description')
        self.assertEqual(fl_tasks[1].columns[1].data, ['Spatial Bandit'])
        self.assertEqual(fl_tasks[1].columns[2].name, 'camera_id')
        self.assertEqual(fl_tasks[1].columns[2].data, [[1, 2]])
        self.assertEqual(fl_tasks[1].columns[3].name, 'task_epochs')
        self.assertEqual(fl_tasks[1].columns[3].data, [[2, 4]])

    @should_raise(TypeError)
    def test_task_manager_failed_due_to_none_param(self):
        task_manager = TaskManager(None)

        task_manager.get_fl_tasks()

    @should_raise(NoneParamException)
    def test_task_manager_get_fl_tasks_failed_due_to_none_task_metadata(self):
        metadata = {"tasks": None}
        task_manager = TaskManager(metadata)

        task_manager.get_fl_tasks()
