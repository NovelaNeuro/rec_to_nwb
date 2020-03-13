import os
import unittest

from fl.datamigration.metadata.metadata_manager import MetadataManager
from fl.datamigration.raw_to_nwb_builder import RawToNWBBuilder

path = os.path.dirname(os.path.abspath(__file__))

_DEFAULT_ANALOG_EXPORT_ARGS = ('-reconfig', str(path) + '/../datamigration/res/reconfig_header.xml')


@unittest.skip("Super heavy RAW to NWB Generation")
class TestRawToNWBGeneration(unittest.TestCase):

    def setUp(self):
        metadata = MetadataManager(
            str(path) + '/../datamigration/res/metadata.yml',
            [
                str(path) + '/../datamigration/res/probe1.yml',
                str(path) + '/../datamigration/res/probe2.yml',
                str(path) + '/../datamigration/res/probe3.yml'
            ]
        )
        self.builder = RawToNWBBuilder(
            animal_name='beans',
            data_path=str(path) + '/../test_data/',
            dates=['20190718'],
            nwb_metadata=metadata,
            output_path='',
            extract_spikes=False,
            extract_mda=True,
            extract_time=True,
            extract_lfps=False,
            extract_analog=True,
            extract_dio=True,
            overwrite=True,
            analog_export_args=_DEFAULT_ANALOG_EXPORT_ARGS
        )

    def test_from_raw_to_nwb_generation(self):
        self.builder.build_nwb()
        self.assertTrue(os.path.exists('beans20190718.nwb'), 'NWBFile did not build')

    def tearDown(self):
        self.builder.cleanup()
