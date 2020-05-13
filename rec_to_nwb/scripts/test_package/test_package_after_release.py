import os
import subprocess
from unittest import TestCase

from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.raw_to_nwb_builder import RawToNWBBuilder

path = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_ANALOG_EXPORT_ARGS = ('-reconfig', str(path) + '/reconfig_header.xml')


class TestPackageAfterRelease(TestCase):

    def setUp(self):
        cmd = subprocess.check_output(str(path)+'/create_conda.sh')
        print(cmd)

    def test_build_and_read_nwb(self):
        metadata = MetadataManager(
            str(path) + '/metadata.yml',
            [str(path) + '/probe1.yml',
             str(path) + '/probe2.yml',
             str(path) + '/probe3.yml'])
        builder = RawToNWBBuilder(
            animal_name='beans',
            data_path='C:/Workspace/Python/fldatamigration/fl/test/test_data/',
            dates=['20190718'],
            nwb_metadata=metadata,
            output_path='',
            associated_files=[],
            extract_spikes=False,
            extract_mda=False,
            extract_lfps=False,
            extract_analog=False,
            extract_dio=False,
            overwrite=False,
            analog_export_args=_DEFAULT_ANALOG_EXPORT_ARGS
        )
        builder.build_nwb()
