import unittest
from datetime import datetime
import os
from dateutil.tz import tzlocal
from src.datamigration.nwb_file_creator import NWBFileCreator


class TestMetadata(unittest.TestCase):

    def setUp(self):
        nwb_builder = NWBFileCreator('John the experimenter',
                                     'novela lab', 'novela institution',
                                     'our novela experiment',
                                     'description of the novela session',
                                     datetime(2019, 10, 31, tzinfo=tzlocal()),
                                     'some novela indentifier'
                                     )
        nwb_builder.build()

    def test_building_nwb(self):
        self.assertNotEqual(0, os.path.getsize('example_file_path.nwb'))
