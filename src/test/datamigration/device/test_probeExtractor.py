import os
import tempfile
from tempfile import tempdir
from unittest import TestCase, mock

import yaml

from src.datamigration.nwb.components.device.probe_extractor import ProbesExtractor

path = os.path.dirname(os.path.abspath(__file__))


# ToDo mock yaml files
class TestProbeExtractor(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.probes_extractor = ProbesExtractor()

        #
        # cls.probes_content = cls.probes_extractor.extract_probes_metadata(
        #     [
        #         path + '/res/probe1.yml',
        #         path + '/res/probe2.yml',
        #         path + '/res/probe3.yml'
        #     ]
        # )

        cls.contents = {
            "foo": "bar",
            "foo2": [
                "testString",
                "testString2"
            ],
            "first": None,
            "second": 1,
            "third": True,
            "emptyArray": [],
            "emptyObject": {},
            "emptyString": ""
        }

        with tempfile.TemporaryDirectory(dir=path) as dirpath:
            testfile = os.path.join(dirpath, 'file1.yml')
            with open(testfile, 'w') as outfile:
                yaml.dump(cls.contents, outfile, default_flow_style=False)
                cls.result = cls.probes_extractor.extract_probes_metadata([dirpath + '/file1.yml'])

    def test_extractProbesMetadata_correctContent_true(self):
        self.assertEqual(self.contents, self.result[0])
