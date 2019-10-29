import os
import unittest


class ProcessingIntegrationTest(unittest.TestCase):

    @unittest.skipIf(os.environ.get("skipProcessingTest") == True,
                     reason="Skipping ProcessingIntegrationTest on Travis CI")
    def processing(self):
        pass
