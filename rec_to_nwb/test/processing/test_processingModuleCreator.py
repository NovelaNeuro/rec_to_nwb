import os
from unittest import TestCase
from unittest.mock import Mock

from hdmf.common.table import DynamicTable

from rec_to_nwb.processing.nwb.components.processing_module.processing_module_creator import ProcessingModuleCreator

path = os.path.dirname(os.path.abspath(__file__))


class TestProcessingModuleCreator(TestCase):

    def test_successfully_insert_task_into_processing_module(self):
        pm_creator = ProcessingModuleCreator('pm_name', 'pm_description')

        mock_dynamic_table = Mock(spec=DynamicTable)
        mock_dynamic_table.name = 'dynamic_name'
        mock_dynamic_table.description = 'dynamic_description'
        mock_dynamic_table.data = []

        pm_creator.insert(mock_dynamic_table)

        self.assertIsNotNone(pm_creator)
        self.assertEqual('dynamic_name', pm_creator.processing_module.data_interfaces['dynamic_name'].name)
        self.assertEqual('dynamic_description',
                         pm_creator.processing_module.data_interfaces['dynamic_name'].description)
        self.assertEqual([], pm_creator.processing_module.data_interfaces['dynamic_name'].data)

    def test_does_not_insert_none_object(self):
        pm_creator = ProcessingModuleCreator('pm_name', 'pm_description')

        pm_creator.insert(None)

        self.assertEqual(0, len(pm_creator.processing_module.children))
