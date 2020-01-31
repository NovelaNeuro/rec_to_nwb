import os
import unittest
from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile

from src.datamigration.nwb_builder.builders.apparatus_builder import ApparatusBuilder
from src.datamigration.nwb_builder.creators.processing_module_creator import ProcessingModuleCreator
from src.datamigration.nwb_builder.injectors.processing_module_injector import ProcessingModuleInjector
from src.datamigration.nwb_builder.managers.processing_module_manager import ProcessingModuleManager
from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata

path = os.path.dirname(os.path.abspath(__file__))


class TestApparatus(unittest.TestCase):

    def setUp(self):
        self.nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )
        self.metadata = NWBMetadata(str(path) + '/res/metadata.yml', []).metadata

    def test_apparatus_creation(self):
        injector = ProcessingModuleInjector(self.nwb_file)
        processing_module = ProcessingModuleCreator.create_processing_module('apparatus', 'apparatus description')
        apparatus_before_injection = ApparatusBuilder(self.metadata).build()
        processing_module_manager = ProcessingModuleManager(processing_module)
        processing_module_manager.add_data(apparatus_before_injection)
        injector.join_processing_module(processing_module)

        return_apparatus = self.nwb_file.processing['apparatus']['apparatus']

        self.assertEqual('apparatus', return_apparatus.name)
        self.assertEqual(apparatus_before_injection.edges, return_apparatus.edges)
        self.assertEqual(apparatus_before_injection.nodes, return_apparatus.nodes)
