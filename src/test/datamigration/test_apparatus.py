import os
import unittest
from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile

from src.datamigration.nwb_builder.builders.apparatus_builder import ApparatusBuilder
from src.datamigration.nwb_builder.builders.processing_module_builder import build_processing_module
from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata

path = os.path.dirname(os.path.abspath(__file__))


class TestExtensions(unittest.TestCase):

    def setUp(self):
        self.nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )
        self.metadata = NWBMetadata(str(path) + '/res/metadata.yml', []).metadata
        build_processing_module(name='apparatus',
                                description='description of apparatus module',
                                nwb_content=self.nwb_file)

    def test_apparatus_creation(self):
        apparatus = ApparatusBuilder(self.metadata, self.nwb_file)
        self.nwb_file.processing['apparatus'].add_data_interface(apparatus.build())
        return_apparatus = self.nwb_file.processing['apparatus']['apparatus']

        self.assertEqual('apparatus', return_apparatus.name)
        self.assertEqual(apparatus.edges, return_apparatus.edges)
        self.assertEqual(apparatus.nodes, return_apparatus.nodes)