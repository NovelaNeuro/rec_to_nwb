import os
from unittest import TestCase

from src.datamigration.extension.apparatus import Apparatus
from src.datamigration.nwb_builder.builders.task_builder import TaskBuilder
from src.datamigration.nwb_builder.creators.processing_module_creator import ProcessingModuleCreator

path = os.path.dirname(os.path.abspath(__file__))


class TestProcessingModuleCreator(TestCase):

    def test_successfully_insert_apparatus_into_processing_module(self):
        pm_creator = ProcessingModuleCreator('pm_name', 'pm_description')
        apparatus = Apparatus(name='apparatus', edges=[], nodes=[])

        pm_creator.insert(apparatus)

        self.assertIsNotNone(pm_creator)
        self.assertEqual('apparatus', pm_creator.processing_module.children[0].name)

    def test_successfully_insert_apparatus_and_task_into_processing_module(self):
        pm_creator = ProcessingModuleCreator('pm_name', 'pm_description')
        apparatus = Apparatus(name='apparatus', edges=[], nodes=[])

        metadata = {"tasks": [{"task_name": "Sleep", "task_description": "The animal sleeps in a small empty box."}]}
        task = TaskBuilder(metadata).build()

        pm_creator.insert(apparatus)
        pm_creator.insert(task)

        self.assertIsNotNone(pm_creator)
        self.assertEqual('apparatus', pm_creator.processing_module.children[0].name)
        self.assertEqual('task', pm_creator.processing_module.children[1].name)

    def test_does_not_insert_none_object(self):
        pm_creator = ProcessingModuleCreator('pm_name', 'pm_description')

        pm_creator.insert(None)

        self.assertEqual(0, len(pm_creator.processing_module.children))
