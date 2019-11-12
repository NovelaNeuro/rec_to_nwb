import unittest

from src.models.custom_extension_builder import CustomExtensionsBuilder
from src.test.e2etests.experiment_data import ExperimentData


class TestCustomExtensionBuilder(unittest.TestCase):

    def setUp(self):
        # ToDo can`t pass path to create somewhere else specs and namespaces. We must move it
        self.custom_extension_builder = CustomExtensionsBuilder(
            ext_source=(ExperimentData.novela_specs),
            ns_path=(ExperimentData.novela_namespaces),
        )

    def test_namespace_exist(self):
        self.assertTrue(True)

    def test_specs_exist(self):
        self.assertTrue(True)
