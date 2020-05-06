import os
import unittest

from testfixtures import should_raise

from fl.processing.metadata.metadata_manager import MetadataManager
from fl.processing.raw_to_nwb_builder import RawToNWBBuilder

path = os.path.dirname(os.path.abspath(__file__))

_DEFAULT_ANALOG_EXPORT_ARGS = ('-reconfig', str(path) + '/../processing/res/reconfig_header.xml')


@unittest.skip("Super heavy RAW to NWB Generation")
class TestRawToNWBGeneration(unittest.TestCase):

    def setUp(self):
        self.metadata = MetadataManager(
            str(path) + '/../processing/res/metadata.yml',
            [
                str(path) + '/../processing/res/probe1.yml',
                str(path) + '/../processing/res/probe2.yml',
                str(path) + '/../processing/res/probe3.yml'
            ]
        )
        self.builder = RawToNWBBuilder(
            animal_name='beans',
            data_path=str(path) + '/../test_data/',
            dates=['20190718'],
            nwb_metadata=self.metadata,
            associated_files=[
                (str(path) + '/processing/res/test_text_files/test1_file'),
                (str(path) + '/processing/res/test_text_files/test2_file'),
            ],
            output_path='',
            extract_spikes=False,
            extract_mda=True,
            extract_lfps=False,
            extract_analog=True,
            extract_dio=True,
            overwrite=True,
            analog_export_args=_DEFAULT_ANALOG_EXPORT_ARGS
        )

    def test_from_raw_to_nwb_generation(self):
        self.builder.build_nwb()
        self.assertTrue(os.path.exists('beans20190718.nwb'), 'NWBFile did not build')

    @should_raise(TypeError)
    def test_raw_to_nwb_builder_failed_due_to_none_parameters(self):
        RawToNWBBuilder(
            animal_name='beans',
            data_path=str(path) + '/../test_data/',
            dates=['20190718'],
            nwb_metadata=None,
            associated_files=[
                (str(path) + '/processing/res/20191212_bill_02_r1.stateScriptLog'),
                (str(path) + '/processing/res/V4_delay_no_home_chinatown_3_4_20.sc'),
                (str(path) + '/processing/res/V4_no_home_light_cue_chinatown_3_4_20.py')
            ]
        )

    @should_raise(TypeError)
    def test_raw_to_nwb_builder_failed_due_to_incorrect_type_parameters(self):
        RawToNWBBuilder(
            animal_name=11111,
            data_path=str(path) + '/../test_data/',
            dates=['20190718'],
            nwb_metadata=self.metadata,
            associated_files=[
                str(path) + '/../processing/res/20191212_bill_02_r1.stateScriptLog',
                str(path) + '/../processing/res/V4_delay_no_home_chinatown_3_4_20.sc',
                str(path) + '/../processing/res/V4_no_home_light_cue_chinatown_3_4_20.py'
            ],
            output_path='',
            extract_spikes=False,
            extract_mda=True,
            extract_lfps=False,
            extract_analog=True,
            extract_dio=True,
            overwrite=True,
            analog_export_args=_DEFAULT_ANALOG_EXPORT_ARGS
        )

    def tearDown(self):
        self.builder.cleanup()
