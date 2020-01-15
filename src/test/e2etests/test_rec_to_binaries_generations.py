import os
import unittest

from rec_to_binaries import extract_trodes_rec_file


class TestRecToBinGeneration(unittest.TestCase):

    def setUp(self):
        pass

    @unittest.skip("Super heavy REC to Preprocessing Generation")
    def test_generation_preprocessing(self):
        extract_trodes_rec_file('test_data/', 'beans', parallel_instances=4)
        self.assertTrue(os.path.isdir('test_data/beans/preprocessing'))
        self.assertTrue(os.path.isdir('test_data/beans/preprocessing/' + "20190718"))
