import os
import unittest
from datetime import datetime

import yaml
from pynwb import NWBFile

from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.electrode_table_builder import ElectrodeTableBuilder


class TestMDAMigration(unittest.TestCase):

    @classmethod
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.nwb_file_content = self.create_test_file()
        self.nwb_file_content.create_electrode_group(
            name='electrode group 3',
            description='description',
            location='location',
            device=self.nwb_file_content.devices['device_name']
        )

        with open(path + '/res/probe_test.yml', 'r') as stream:
            probe_dict = yaml.safe_load(stream)
        probes = [probe_dict]
        header = Header(path + '/res/header_test.xml')
        self.table_builder = ElectrodeTableBuilder(self.nwb_file_content, probes,
                                                   self.nwb_file_content.electrode_groups, header)

    def test_electrode_table(self):
        print(self.nwb_file_content.electrodes)
        self.assertTrue(1)
        # add test there

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
        return nwb_file_content
