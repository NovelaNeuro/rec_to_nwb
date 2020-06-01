import os
from pathlib import Path
from unittest import TestCase

import pynwb

from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.builder.raw_to_nwb_builder import RawToNWBBuilder

path = Path(__file__).parent.parent
path.resolve()
_DEFAULT_TRODES_REC_EXPORT_ARGS = (
    '-reconfig',
    str(path) + '/rec_to_nwb/rec_to_nwb/test/processing/res/reconfig_header.xml'
)


class TestPackageAfterRelease(TestCase):
    """Class created to normalize testing.
    1. Copy 'test package' folder to the same catalog as the project is.
    2. Run create_conda.sh from terminal.
    3. Set Python interpreter to created environment
    4. Run test_build_and_read_nwb
    """

    def test_build_and_read_nwb(self):
        metadata = MetadataManager(
            str(path) + '/rec_to_nwb/rec_to_nwb/test/processing/res/metadata.yml',
            [str(path) + '/rec_to_nwb/rec_to_nwb/test/processing/res/probe1.yml',
             str(path) + '/rec_to_nwb/rec_to_nwb/test/processing/res/probe2.yml',
             str(path) + '/rec_to_nwb/rec_to_nwb/test/processing/res/probe3.yml'])
        builder = RawToNWBBuilder(
            animal_name='beans',
            data_path=str(path) + '/rec_to_nwb/rec_to_nwb/test/test_data/',
            dates=['20190718'],
            nwb_metadata=metadata,
            output_path='',
            extract_spikes=False,
            extract_mda=True,
            extract_lfps=False,
            extract_analog=True,
            extract_dio=True,
            overwrite=True,
            trodes_rec_export_args=_DEFAULT_TRODES_REC_EXPORT_ARGS
        )
        builder.build_nwb()

        self.assertTrue(os.path.exists('beans20190718.nwb'))
        with pynwb.NWBHDF5IO('beans20190718.nwb', 'r', load_namespaces=True) as nwb_file_handler:
            nwb_file = nwb_file_handler.read()
            print(nwb_file)

        if os.path.isfile('beans20190718.nwb'):
            os.remove('beans20190718.nwb')
