import os
import unittest


class ProcessingIntegrationTest(unittest.TestCase):

    @unittest.skipIf(os.environ.get("TRAVIS") is not None,
                     reason="Skipping ProcessingIntegrationTest on Travis CI")
    def test_processing_integration(self):
        assert 1 == 1

    def test_2processing_integration(self):
        assert 2 == 2
