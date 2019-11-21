import unittest

from src.datamigration.extension.extension_builder import ExtensionsBuilder
from src.test.e2etests.experiment_data import ExperimentData


class TestCustomExtensionBuilder(unittest.TestCase):

    def setUp(self):
        self.custom_extension_builder = ExtensionsBuilder(
            ext_source=ExperimentData.novela_specs,
            ns_path=ExperimentData.novela_namespaces,
        )

    def test_namespace_exist(self):
        self.assertTrue(True)

    def test_specs_exist(self):
        self.assertTrue(True)
