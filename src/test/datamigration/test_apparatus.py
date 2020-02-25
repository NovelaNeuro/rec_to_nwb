import os
from unittest import TestCase

from src.datamigration.nwb.components.apparatus.apparatus_builder import ApparatusBuilder
from src.datamigration.nwb.components.processing_module.processing_module_creator import ProcessingModuleCreator

path = os.path.dirname(os.path.abspath(__file__))


class TestApparatus(TestCase):

    def test_apparatus_creation(self):
        apparatus_metadata = [
                              [1, 0, 1, 0, 1],
                              [1, 0, 1, 1, 1],
                              [1, 0, 0, 1, 0],
                              [0, 1, 0, 0, 1],
                              [0, 1, 1, 0, 1]
                              ]
        pm_creator = ProcessingModuleCreator('apparatus', 'description')
        apparatus = ApparatusBuilder(apparatus_metadata).build()

        pm_creator.insert(apparatus)

        return_apparatus = pm_creator.processing_module.children[0]

        self.assertEqual('apparatus', return_apparatus.name)
        self.assertEqual(apparatus.edges, return_apparatus.edges)
        self.assertEqual(apparatus.nodes, return_apparatus.nodes)
