import os
import tempfile
from tempfile import tempdir
from unittest import TestCase, mock

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

    def test_LoadOperation(self):
        contents = "---\nfoo: blargh\nblee:\n - blah\n - blorp\n"

        with tempfile.TemporaryDirectory(dir=path) as dirpath:
            testfile = os.path.join(dirpath, 'file1')
            with open(testfile, 'w') as outfile:
                outfile.write(contents)

            with mock.patch('yaml.safe_load') as safe_load:
                def loader(f):
                    safe_load.file_contents = f.read()
                    return safe_load.return_value


                safe_load.side_effect = loader
                result = self.probes_extractor.extract_probes_metadata(testfile)

                # yaml.safe_load called once
                self.assertEqual(1, len(safe_load.call_args_list))
                self.assertEqual(contents, safe_load.file_contents)
                self.assertEqual(result, safe_load.return_value)

    # def test_extractProbesMetadata_successful_true(self):
    #     self.assertIsNotNone(self.probes_content)
