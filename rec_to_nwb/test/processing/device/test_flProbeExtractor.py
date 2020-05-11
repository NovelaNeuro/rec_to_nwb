import os
import tempfile
from tempfile import tempdir
from unittest import TestCase, mock

import yaml

from rec_to_nwb.processing.nwb.components.device.fl_probe_extractor import FlProbesExtractor

path = os.path.dirname(os.path.abspath(__file__))


class TestFlProbeExtractor(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fl_probes_extractor = FlProbesExtractor()

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

                cls.result = cls.fl_probes_extractor.extract_probes_metadata([dirpath + '/file1.yml'])

    def test_extractProbesMetadata_correctContent_true(self):
        self.assertEqual(self.contents, self.result[0])
