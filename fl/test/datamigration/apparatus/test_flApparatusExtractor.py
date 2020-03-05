from unittest import TestCase

from ndx_fllab_novela.apparatus import Node, Edge

from fl.datamigration.nwb.components.apparatus.fl_apparatus_extractor import FlApparatusExtractor


class TestFlApparatusExtractor(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.apparatus_metadata = [
            [1, 0, 1, 0, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1],
            [0, 1, 1, 0, 1]
        ]

        cls.fl_apparatus_extractor = FlApparatusExtractor(cls.apparatus_metadata)
        cls.edges, cls.nodes = cls.fl_apparatus_extractor.get_data()

    def test_getData_successfulCreated_true(self):
        self.assertIsNotNone(self.edges)
        self.assertIsNotNone(self.nodes)

    def test_getData_returnCorrectTypes_true(self):
        self.assertIsInstance(self.edges, list)
        self.assertIsInstance(self.edges[0], Edge)

        self.assertIsInstance(self.nodes, list)
        self.assertIsInstance(self.nodes[0], Node)

