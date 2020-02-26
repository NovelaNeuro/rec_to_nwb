from unittest import TestCase
from unittest.mock import Mock

from src.datamigration.nwb.components.apparatus.apparatus_extractor import ApparatusExtractor
from src.datamigration.nwb.components.apparatus.apparatus_manager import ApparatusManager
from src.datamigration.nwb.components.apparatus.lf_apparatus import LfApparatus


class TestApparatusManager(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.apparatus_metadata = Mock(spec=dict)

        cls.apparatus_manager = ApparatusManager(cls.apparatus_metadata)
        cls.apparatus_manager.apparatus_extractor = Mock(spec=ApparatusExtractor)
        cls.apparatus_manager.apparatus_extractor.get_data.return_value =

        cls.lf_apparatus = cls.apparatus_manager.get_lf_apparatus()

    def test_getLfApparatus_successfulCreated_true(self):
        self.assertIsNotNone(self.lf_apparatus)

    def test_getLfApparatus_returnCorrectValues_true(self):
        self.assertEqual(self.lf_apparatus)

    def test_getLfApparatus_returnCorrectTypes_true(self):
        self.assertIsInstance(self.lf_apparatus, LfApparatus)