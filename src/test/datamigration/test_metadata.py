import os
import unittest

import pytz
from pynwb.epoch import TimeIntervals
from pynwb.file import Subject

from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor

path = os.path.dirname(os.path.abspath(__file__))


class TestMetadata(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.metadata = MetadataExtractor(config_path=path + '/res/metadata.yml')

    def test_reading_rec_link(self):
        self.assertIsNotNone(self.metadata.link_to_rec)
        self.assertEqual('https://drive.google.com/open?id=1jIsDYgNsrmEDkFT0XLlIZY3LwVDLXa7H',
                         self.metadata.link_to_rec)

    def test_reading_base_metadata(self):
        self.assertEqual('hulk', self.metadata.experimenter_name)
        self.assertEqual('hulk`s lab', self.metadata.lab)
        self.assertEqual('stark industrice', self.metadata.institution)
        self.assertEqual('project avengers', self.metadata.experiment_description)
        self.assertEqual('winter soldier', self.metadata.session_description)
        self.assertEqual(12345, self.metadata.identifier)
        self.assertEqual('10/31/2019, 20:15:30', self.metadata.session_start_time.strftime("%m/%d/%Y, %H:%M:%S"))

    def test_reading_subject(self):
        self.assertIsNotNone(self.metadata.subject)
        self.assertIsInstance(self.metadata.subject, Subject)
        self.assertEqual('23', self.metadata.subject.age)
        self.assertEqual('big bad thanos', self.metadata.subject.description)
        self.assertEqual('who knows', self.metadata.subject.genotype)
        self.assertEqual('female', self.metadata.subject.sex)
        self.assertEqual('eternal deviant hybrid', self.metadata.subject.species)
        self.assertEqual('Th1', self.metadata.subject.subject_id)
        self.assertEqual('120', self.metadata.subject.weight)
        self.assertEqual('06/16/2001', self.metadata.subject.date_of_birth.strftime("%m/%d/%Y"))
        self.assertEqual(pytz.timezone("America/Los_Angeles").zone, self.metadata.subject.date_of_birth.tzinfo.zone)

    def test_reading_task(self):
        """
        We take slices self.metadata.task['start_time'][:],
        we also can take first element: self.metadata.task['start_time'][0],
        but can`t take whole object self.metadata.task['start_time']
        """
        self.assertIsNotNone(self.metadata.task)
        self.assertIsInstance(self.metadata.task, TimeIntervals)
        self.assertEqual('novela task', self.metadata.task.name)
        self.assertEqual('some description', self.metadata.task.description)
        self.assertEqual(('start_time', 'stop_time', 'tags'), self.metadata.task.colnames)
        self.assertEqual([1.0], self.metadata.task['start_time'][:])
        self.assertEqual([24.0], self.metadata.task['stop_time'][:])
        self.assertEqual([['some tag']], self.metadata.task['tags'][:])

    def test_reading_device(self):
        self.assertIsNotNone(self.metadata.devices)
        self.assertIsInstance(self.metadata.devices, list)
        self.assertIsInstance(self.metadata.devices[0], str)
        self.assertEqual(['dev1', 'dev2', 'dev3'], self.metadata.devices)

    def test_reading_electrode_group(self):
        self.assertIsNotNone(self.metadata.electrode_groups)
        self.assertIsInstance(self.metadata.electrode_groups, list)

        self.assertEqual('electrode group 1', self.metadata.electrode_groups[0]['name'])
        self.assertEqual('some description 1', self.metadata.electrode_groups[0]['description'])
        self.assertEqual('some location 1', self.metadata.electrode_groups[0]['location'])
        self.assertEqual('dev1', self.metadata.electrode_groups[0]['device'])

        self.assertEqual('electrode group 2', self.metadata.electrode_groups[1]['name'])
        self.assertEqual('some description 2', self.metadata.electrode_groups[1]['description'])
        self.assertEqual('some location 2', self.metadata.electrode_groups[1]['location'])
        self.assertEqual('dev2', self.metadata.electrode_groups[1]['device'])

    def test_reading_electrode(self):
        self.assertIsNotNone(self.metadata.electrodes)
        self.assertIsInstance(self.metadata.electrodes, list)

        self.assertEqual(1.0, self.metadata.electrodes[0]['x'])
        self.assertEqual(1.0, self.metadata.electrodes[0]['y'])
        self.assertEqual(1.0, self.metadata.electrodes[0]['z'])
        self.assertEqual(3.0, self.metadata.electrodes[0]['imp'])
        self.assertEqual('hippocampus', self.metadata.electrodes[0]['location'])
        self.assertEqual('no filter', self.metadata.electrodes[0]['filtering'])
        self.assertEqual('electrode group 1', self.metadata.electrodes[0]['group'])
        self.assertEqual(1, self.metadata.electrodes[0]['id'])

        self.assertEqual(2.0, self.metadata.electrodes[1]['x'])
        self.assertEqual(2.0, self.metadata.electrodes[1]['y'])
        self.assertEqual(2.0, self.metadata.electrodes[1]['z'])
        self.assertEqual(5.0, self.metadata.electrodes[1]['imp'])
        self.assertEqual('neocortex', self.metadata.electrodes[1]['location'])
        self.assertEqual('yes filter', self.metadata.electrodes[1]['filtering'])
        self.assertEqual('electrode group 2', self.metadata.electrodes[1]['group'])
        self.assertEqual(2, self.metadata.electrodes[1]['id'])

        self.assertEqual(1.0, self.metadata.electrodes[2]['x'])
        self.assertEqual(1.0, self.metadata.electrodes[2]['y'])
        self.assertEqual(1.0, self.metadata.electrodes[2]['z'])
        self.assertEqual(3.0, self.metadata.electrodes[2]['imp'])
        self.assertEqual('hippocampus', self.metadata.electrodes[2]['location'])
        self.assertEqual('no filter', self.metadata.electrodes[2]['filtering'])
        self.assertEqual('electrode group 1', self.metadata.electrodes[2]['group'])
        self.assertEqual(3, self.metadata.electrodes[2]['id'])

        self.assertEqual(2.0, self.metadata.electrodes[3]['x'])
        self.assertEqual(2.0, self.metadata.electrodes[3]['y'])
        self.assertEqual(2.0, self.metadata.electrodes[3]['z'])
        self.assertEqual(5.0, self.metadata.electrodes[3]['imp'])
        self.assertEqual('neocortex', self.metadata.electrodes[3]['location'])
        self.assertEqual('yes filter', self.metadata.electrodes[3]['filtering'])
        self.assertEqual('electrode group 2', self.metadata.electrodes[3]['group'])
        self.assertEqual(4, self.metadata.electrodes[3]['id'])

    def test_reading_electrode_region(self):
        self.assertIsNotNone(self.metadata.electrode_regions)
        self.assertIsInstance(self.metadata.electrode_regions, list)

        self.assertEqual('region 1', self.metadata.electrode_regions[0]['name'])
        self.assertEqual('description 1', self.metadata.electrode_regions[0]['description'])
        self.assertEqual([0, 1], self.metadata.electrode_regions[0]['region'])

        self.assertEqual('region 2', self.metadata.electrode_regions[1]['name'])
        self.assertEqual('description 2', self.metadata.electrode_regions[1]['description'])
        self.assertEqual([1], self.metadata.electrode_regions[1]['region'])

    def test_reading_apparatus(self):
        self.assertIsNotNone(self.metadata.apparatus)
        self.assertIsInstance(self.metadata.apparatus, list)
        self.assertEqual(1, self.metadata.apparatus[0][0])
        self.assertEqual([1, 0, 1, 0, 1], self.metadata.apparatus[0])
        self.assertEqual(
            [
                [1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1],
                [1, 0, 0, 1, 0],
                [0, 1, 0, 0, 1],
                [0, 1, 1, 0, 1]
            ], self.metadata.apparatus[:])
