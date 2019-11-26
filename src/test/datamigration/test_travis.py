import unittest
from datetime import datetime

from pynwb import NWBFile


class TestTravis(unittest.TestCase):
    def test_travis(self):
        nwb_file_content = NWBFile(session_description='session_description',
                                   experimenter='experimenter_name',
                                   lab='lab',
                                   institution='institution',
                                   session_start_time=datetime(2017, 4, 3, 11),
                                   identifier='identifier',
                                   experiment_description='experiment_description'
                                   )
        self.assertIsNotNone(1)
