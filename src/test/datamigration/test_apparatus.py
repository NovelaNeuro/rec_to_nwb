import os
from unittest import TestCase

from src.datamigration.nwb_builder.builders.apparatus_builder import ApparatusBuilder
from src.datamigration.nwb_builder.creators.processing_module_creator import ProcessingModuleCreator
from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata

path = os.path.dirname(os.path.abspath(__file__))


class TestApparatus(TestCase):

    def test_apparatus_creation(self):
        self.metadata = NWBMetadata(str(path) + '/res/metadata.yml',
                                    []).metadata  # todo there is no need to test it with metadata.yml file at all, please build apparatus inline here
                                                    # Aparratus need to be built basing on yml file(we can refactor whole metadata processing)
        pm_creator = ProcessingModuleCreator('p_module', 'description')
        apparatus = ApparatusBuilder(self.metadata).build()

        pm_creator.insert(apparatus)

        return_apparatus = pm_creator.processing_module.children[0]

        self.assertEqual('apparatus', return_apparatus.name)
        self.assertEqual(apparatus.edges, return_apparatus.edges)
        self.assertEqual(apparatus.nodes, return_apparatus.nodes)
