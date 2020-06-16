import os
from unittest import TestCase

from rec_to_nwb.processing.nwb.components.processing_module.processing_module_creator import ProcessingModuleCreator
from rec_to_nwb.processing.nwb.components.task.task_builder import TaskBuilder

path = os.path.dirname(os.path.abspath(__file__))


class TestProcessingModuleCreator(TestCase):

    def test_successfully_insert_task_into_processing_module(self):
        pm_creator = ProcessingModuleCreator('pm_name', 'pm_description')
        metadata = {"tasks": [
            {"task_name": "Sleep", "task_description": "The animal sleeps in a small empty box.",
             'camera_id': [0], 'task_epochs': [1, 3, 5]},
            {"task_name": "Stem+Leaf", "task_description": "Spatial Bandit",
             'camera_id': [1, 2], 'task_epochs': [2, 4]},
        ]}
        task = TaskBuilder(metadata).build()

        pm_creator.insert(task)

        self.assertIsNotNone(pm_creator)
        self.assertEqual('task', pm_creator.processing_module.children[0].name)

    def test_does_not_insert_none_object(self):
        pm_creator = ProcessingModuleCreator('pm_name', 'pm_description')

        pm_creator.insert(None)

        self.assertEqual(0, len(pm_creator.processing_module.children))
