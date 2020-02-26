from unittest import TestCase
from unittest.mock import Mock

from src.datamigration.nwb.components.apparatus.lf_apparatus_extractor import LfApparatusExtractor
from src.datamigration.nwb.components.apparatus.lf_apparatus_manager import LfApparatusManager
from src.datamigration.nwb.components.apparatus.lf_apparatus import LfApparatus


class TestLfApparatusManager(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.apparatus_metadata = Mock(spec=dict)

        edges = Mock(spec=list)
        nodes = Mock(spec=list)

        cls.lf_apparatus_manager = LfApparatusManager(cls.apparatus_metadata)
        cls.lf_apparatus_manager.apparatus_extractor = Mock(spec=LfApparatusExtractor)
        cls.lf_apparatus_manager.apparatus_extractor.get_data.return_value = edges, nodes

        cls.predicted_result = LfApparatus(edges, nodes)
        cls.lf_apparatus = cls.lf_apparatus_manager.get_lf_apparatus()

    def test_getLfApparatus_successfulCreated_true(self):
        self.assertIsNotNone(self.lf_apparatus)

    def test_getLfApparatus_returnCorrectValues_true(self):
        self.assertEqual(self.lf_apparatus.edges, self.predicted_result.edges)
        self.assertEqual(self.lf_apparatus.nodes, self.predicted_result.nodes)

    def test_getLfApparatus_returnCorrectTypes_true(self):
        self.assertIsInstance(self.lf_apparatus, LfApparatus)