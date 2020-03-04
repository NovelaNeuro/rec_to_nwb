from unittest import TestCase

from ndx_lflab_novela.apparatus import Node, Edge

from src.datamigration.nwb.components.apparatus.lf_apparatus_extractor import LfApparatusExtractor


class TestLfApparatusExtractor(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.apparatus_metadata = [
            [1, 0, 1, 0, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1],
            [0, 1, 1, 0, 1]
        ]

        cls.lf_apparatus_extractor = LfApparatusExtractor(cls.apparatus_metadata)
        cls.edges, cls.nodes = cls.lf_apparatus_extractor.get_data()

    def test_getData_successfulCreated_true(self):
        self.assertIsNotNone(self.edges)
        self.assertIsNotNone(self.nodes)

    def test_getData_returnCorrectTypes_true(self):
        self.assertIsInstance(self.edges, list)
        self.assertIsInstance(self.edges[0], Edge)

        self.assertIsInstance(self.nodes, list)
        self.assertIsInstance(self.nodes[0], Node)

