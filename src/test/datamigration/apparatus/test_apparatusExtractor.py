from unittest import TestCase

from ndx_franklab_novela.apparatus import Node, Edge

from src.datamigration.nwb.components.apparatus.apparatus_extractor import ApparatusExtractor


class TestApparatusExtractor(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.apparatus_metadata = [
            [1, 0, 1, 0, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1],
            [0, 1, 1, 0, 1]
        ]

        cls.apparatus_extractor = ApparatusExtractor(cls.apparatus_metadata)
        cls.edges, cls.nodes = cls.apparatus_extractor.get_data()

    def test_getData_successfulCreated_true(self):
        self.assertIsNotNone(self.edges)
        self.assertIsNotNone(self.nodes)

    def test_getData_returnCorrectTypes_true(self):
        self.assertIsInstance(self.edges, list)
        self.assertIsInstance(self.edges[0], Edge)

        self.assertIsInstance(self.nodes, list)
        self.assertIsInstance(self.nodes[0], Node)

