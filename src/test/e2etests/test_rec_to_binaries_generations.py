import os
import unittest

from rec_to_binaries import extract_trodes_rec_file


class TestRecToBinGeneration(unittest.TestCase):

    def setUp(self):
        pass

    @unittest.skip("Super heavy REC to Preprocessing Generation")
    def test_generation_preprocessing(self):
        extract_trodes_rec_file('testdata/', 'beans', parallel_instances=4)
        self.assertTrue(os.path.isdir('testdata/beans/preprocessing'))
        self.assertTrue(os.path.isdir('testdata/beans/preprocessing' + "20190718"))
