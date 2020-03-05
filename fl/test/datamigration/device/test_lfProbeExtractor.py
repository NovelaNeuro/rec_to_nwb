import os
import tempfile
from tempfile import tempdir
from unittest import TestCase, mock

import yaml

from fl.datamigration.nwb.components.device.lf_probe_extractor import LfProbesExtractor

path = os.path.dirname(os.path.abspath(__file__))


class TestLfProbeExtractor(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.lf_probes_extractor = LfProbesExtractor()

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

                cls.result = cls.lf_probes_extractor.extract_probes_metadata([dirpath + '/file1.yml'])

    def test_extractProbesMetadata_correctContent_true(self):
        self.assertEqual(self.contents, self.result[0])
