import os
import unittest
from pathlib import Path

from rec_to_binaries import extract_trodes_rec_file

path = os.path.dirname(os.path.abspath(__file__))

_DEFAULT_ANALOG_EXPORT_ARGS = ('-reconfig', str(path) + '../datamigration/res/reconfig_header.xml')


class TestRecToBinGeneration(unittest.TestCase):

    # @unittest.skip("Super heavy REC to Preprocessing Generation")
    def test_generation_preprocessing(self):
        extract_trodes_rec_file(
            '../test_data/',
            'beans',
            parallel_instances=4,
            analog_export_args=_DEFAULT_ANALOG_EXPORT_ARGS,
            overwrite=True,
        )
        self.assertTrue(os.path.isdir('../test_data/beans/preprocessing'))
        self.assertTrue(os.path.isdir('../test_data/beans/preprocessing/' + "20190718"))
