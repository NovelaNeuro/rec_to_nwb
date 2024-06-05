import os
import unittest

from testfixtures import should_raise

from rec_to_nwb.processing.builder.raw_to_nwb_builder import RawToNWBBuilder
from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager

path = os.path.dirname(os.path.abspath(__file__))

_DEFAULT_TRODES_REC_EXPORT_ARGS = ('-reconfig', 'C:/Users/wmery/PycharmProjects/rec_to_nwb/rec_to_nwb/test/test_data/KF2/raw/20170120/kf2_reconfig.xml')


#@unittest.skip("Super heavy RAW to NWB Generation")
class TestRawToNWBGeneration(unittest.TestCase):

    def setUp(self):
        self.metadata = MetadataManager(
            'C:/Users/wmery/PycharmProjects/rec_to_nwb/rec_to_nwb/test/test_data/KF2/raw/20170120/kibbles20170216_metadata.yml',
            [
                'C:/Users/wmery/PycharmProjects/rec_to_nwb/rec_to_nwb/test/test_data/KF2/raw/20170120/64c-3s6mm6cm-20um-40um-sl.yml',
                'C:/Users/wmery/PycharmProjects/rec_to_nwb/rec_to_nwb/test/test_data/KF2/raw/20170120/64c-4s6mm6cm-20um-40um-dl.yml'
                ])
        self.builder = RawToNWBBuilder(
            animal_name='KF2',
            data_path=str(path) + '/../test_data/',
            dates=['20170120'],
            nwb_metadata=self.metadata,
            output_path='',
            video_path=str(path) + '/../test_data',
            extract_spikes=False,
            extract_mda=True,
            extract_lfps=False,
            extract_analog=True,
            extract_dio=True,
            overwrite=True,
            trodes_rec_export_args=_DEFAULT_TRODES_REC_EXPORT_ARGS
        )

    def test_from_raw_to_nwb_generation(self):
        self.builder.build_nwb(
            process_mda_valid_time=False,
            process_mda_invalid_time=False,
            process_pos_valid_time=False,
            process_pos_invalid_time=False
        )
        self.assertTrue(os.path.exists('beans20190718.nwb'), 'NWBFile did not build')

    @should_raise(TypeError)
    def test_raw_to_nwb_builder_failed_due_to_none_parameters(self):
        RawToNWBBuilder(
            animal_name='beans',
            data_path=str(path) + '/../test_data/',
            dates=['20190718'],
            nwb_metadata=None,

        )

    @should_raise(TypeError)
    def test_raw_to_nwb_builder_failed_due_to_incorrect_type_parameters(self):
        RawToNWBBuilder(
            animal_name=11111,
            data_path=str(path) + '/../test_data/',
            dates=['20190718'],
            nwb_metadata=self.metadata,
            output_path='',
            extract_spikes=False,
            extract_mda=True,
            extract_lfps=False,
            extract_analog=True,
            extract_dio=True,
            overwrite=True,
            trodes_rec_export_args=_DEFAULT_TRODES_REC_EXPORT_ARGS
        )

    # def tearDown(self):
    #     self.builder.cleanup()
