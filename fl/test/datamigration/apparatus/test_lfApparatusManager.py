from unittest import TestCase
from unittest.mock import Mock

from fl.datamigration.nwb.components.apparatus.fl_apparatus_extractor import LfApparatusExtractor
from fl.datamigration.nwb.components.apparatus.fl_apparatus_manager import LfApparatusManager
from fl.datamigration.nwb.components.apparatus.fl_apparatus import LfApparatus


class TestLfApparatusManager(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.apparatus_metadata = Mock(spec=dict)

        edges = Mock(spec=list)
        nodes = Mock(spec=list)

        cls.fl_apparatus_manager = LfApparatusManager(cls.apparatus_metadata)
        cls.fl_apparatus_manager.fl_apparatus_extractor = Mock(spec=LfApparatusExtractor)
        cls.fl_apparatus_manager.fl_apparatus_extractor.get_data.return_value = edges, nodes

        cls.predicted_result = LfApparatus(edges, nodes)
        cls.fl_apparatus = cls.fl_apparatus_manager.get_fl_apparatus()

    def test_getLfApparatus_successfulCreated_true(self):
        self.assertIsNotNone(self.fl_apparatus)

    def test_getLfApparatus_returnCorrectValues_true(self):
        self.assertEqual(self.fl_apparatus.edges, self.predicted_result.edges)
        self.assertEqual(self.fl_apparatus.nodes, self.predicted_result.nodes)

    def test_getLfApparatus_returnCorrectTypes_true(self):
        self.assertIsInstance(self.fl_apparatus, LfApparatus)