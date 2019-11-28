import os
import unittest

import pytz

from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor

path = os.path.dirname(os.path.abspath(__file__))


class TestMetadata(unittest.TestCase):

    def setUp(self):
        self.metadata = MetadataExtractor(config_path=path + '/res/metadata.yml')

    def test_reading_base_metadata(self):
        self.assertEqual('hulk', self.metadata.experimenter_name)
        self.assertEqual('hulk`s lab', self.metadata.lab)
        self.assertEqual('project avengers', self.metadata.experiment_description)
        self.assertEqual('winter soldier', self.metadata.session_description)
        self.assertEqual(12345, self.metadata.identifier)
        self.assertEqual('10/31/2019, 20:15:30', self.metadata.session_start_time.strftime("%m/%d/%Y, %H:%M:%S"))

    def test_reading_subject(self):
        self.assertIsNotNone(self.metadata.subject)
        self.assertEqual('23', self.metadata.subject.age)
        self.assertEqual('big bad thanos', self.metadata.subject.description)
        self.assertEqual('who knows', self.metadata.subject.genotype)
        self.assertEqual('female', self.metadata.subject.sex)
        self.assertEqual('eternal deviant hybrid', self.metadata.subject.species)
        self.assertEqual('Th1', self.metadata.subject.subject_id)
        self.assertEqual('120', self.metadata.subject.weight)
        self.assertEqual('06/16/2001', self.metadata.subject.date_of_birth.strftime("%m/%d/%Y"))
        self.assertEqual(pytz.timezone("America/Los_Angeles").zone, self.metadata.subject.date_of_birth.tzinfo.zone)

    # todo implement after filling the examples
    def test_reading_task(self):
        pass

    # todo add missing tests for the new fields
