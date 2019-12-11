import os
import unittest
from datetime import datetime

import numpy as np
from pynwb import NWBFile

from src.datamigration.nwb_builder.mda_extractor import MdaExtractor


class TestMDAMigration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.dirname(os.path.abspath(__file__))
        cls.create_test_file()

    def test_reading_mda(self):
        nwb_file_content = self.create_test_file()
        electrode_table_region = nwb_file_content.create_electrode_table_region([0], "sample description")
        timestamps = [self.path + '/res/mda_test/test.timestamps.mda']
        mda_files = [[self.path + '/res/mda_test/test' + str(i) + '.mda' for i in range(1, 4)]]
        mda_extractor = MdaExtractor(mda_files, timestamps)
        series = mda_extractor.get_mda(electrode_table_region)
        self.assertEqual(100, np.size(series.timestamps, 0))
        self.assertEqual(12, np.size(series.data, 1))
        self.assertEqual(5, np.size(series.data, 0))

    @staticmethod
    def create_test_file():
        nwb_file_content = NWBFile(session_description='session_description',
                                   experimenter='experimenter_name',
                                   lab='lab',
                                   institution='institution',
                                   session_start_time=datetime(2017, 4, 3, 11),
                                   identifier='identifier',
                                   experiment_description='experiment_description'
                                   )
        nwb_file_content.create_device(name='device_name')
        nwb_file_content.create_electrode_group(
            name='group_name',
            description='description',
            location='location',
            device=nwb_file_content.devices['device_name']
        )

        nwb_file_content.add_electrode(
            x=1.0,
            y=1.0,
            z=1.0,
            imp=1.0,
            location='location',
            filtering='filtering',
            group=nwb_file_content.electrode_groups['group_name'],
            id=1
        )

        return nwb_file_content
