import unittest
from datetime import datetime

from pynwb import NWBFile

from src.datamigration.nwb_builder.mda_extractor import MdaExtractor
from src.test.e2etests.experiment_data import ExperimentData


class TestMDAMigration(unittest.TestCase):

    def setUp(self):
        self.create_test_file()

    # @unittest.skip("DOES NOT WORK!!!")
    def test_reading_mda(self):
        self.create_test_file()
        # with NWBHDF5IO(path='mda_test.nwb', mode='r') as io:
        # nwb_file = io.read()
        # print(nwb_file)

    def create_test_file(self):
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

        electrode_table_region = nwb_file_content.create_electrode_table_region([0], "sample description")
        mda_extractor = MdaExtractor(ExperimentData.mda_path, ExperimentData.mda_timestamp)
        series = mda_extractor.get_mda(1, mda_data_chunk_size, electrode_table_region, 1)
        nwb_fileIO.add_acquisition(series)
