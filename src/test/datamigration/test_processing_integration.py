import os
import unittest


class ProcessingIntegrationTest(unittest.TestCase):

    @unittest.skipIf(os.environ.get("skipProcessingTest") is not True,
                     reason="Skipping ProcessingIntegrationTest on Travis CI")
    def test_processing_integration(self):
        assert 1 == 1

    def test_2processing_integration(self):
        assert 2 == 2
