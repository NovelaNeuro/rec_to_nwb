import logging.config
import os
import unittest

from rec_to_binaries import extract_trodes_rec_file

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TestRecToBinGeneration(unittest.TestCase):

    @unittest.skip("Super heavy REC to Preprocessing Generation")
    def test_generation_preprocessing(self):
        extract_trodes_rec_file('test_data/', 'beans', parallel_instances=4)
        self.assertTrue(os.path.isdir('test_data/beans/preprocessing'))
        self.assertTrue(os.path.isdir('test_data/beans/preprocessing/' + "20190718"))
