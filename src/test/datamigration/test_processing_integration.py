import os
import unittest


class ProcessingIntegrationTest(unittest.TestCase):

    @unittest.skipIf(os.environ.get("skipProcessingTest") == True,
                     reason="Skipping ProcessingIntegrationTest on Travis CI")
    def test_processing_integration(self):
        assert 1 == 1
