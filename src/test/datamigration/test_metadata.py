import os
from unittest import TestCase

from src.datamigration.nwb_builder.managers.metadata_manager import MetadataManager

path = os.path.dirname(os.path.abspath(__file__))


class TestMetadata(TestCase):

    def setUp(self):
        self.nwb_metadata = MetadataManager(str(path) + '/res/metadata.yml',
                                            [str(path) + '/res/probe1.yml',
                                      str(path) + '/res/probe2.yml',
                                      str(path) + '/res/probe3.yml'
                                      ])

    def test_reading_metadata_fields(self):
        metadata_fields = self.nwb_metadata.metadata.keys()
        self.assertIn('experimenter name', metadata_fields)
        self.assertIn('lab', metadata_fields)
        self.assertIn('institution', metadata_fields)
        self.assertIn('experiment description', metadata_fields)
        self.assertIn('session description', metadata_fields)
        self.assertIn('session_id', metadata_fields)
        self.assertIn('session start time', metadata_fields)
        self.assertIn('subject', metadata_fields)
        self.assertIn('electrode region', metadata_fields)
        self.assertIn('apparatus', metadata_fields)
        self.assertIn('tasks', metadata_fields)
        self.assertIn('behavioral_events', metadata_fields)
        self.assertIn('electrode groups', metadata_fields)
        self.assertIn('ntrode probe channel map', metadata_fields)

    def test_reading_subject(self):
        subject_fields = self.nwb_metadata.metadata['subject'].keys()
        self.assertIn('description', subject_fields)
        self.assertIn('genotype', subject_fields)
        self.assertIn('sex', subject_fields)
        self.assertIn('species', subject_fields)
        self.assertIn('subject id', subject_fields)
        self.assertIn('weight', subject_fields)

    def test_reading_tasks_field(self):
        tasks_fields = self.nwb_metadata.metadata['tasks'][0].keys()
        self.assertIn('task_description', tasks_fields)
        self.assertIn('task_name', tasks_fields)

    def test_reading_behavioral_events_field(self):
        behavioral_event_fields = self.nwb_metadata.metadata['behavioral_events'][0].keys()
        self.assertIn('description', behavioral_event_fields)
        self.assertIn('name', behavioral_event_fields)

    def test_reading_electrode_groups_field(self):
        electrode_groups_fields = self.nwb_metadata.metadata['electrode groups'][0].keys()
        self.assertIn('id', electrode_groups_fields)
        self.assertIn('location', electrode_groups_fields)
        self.assertIn('device_type', electrode_groups_fields)
        self.assertIn('description', electrode_groups_fields)

    def test_reading_ntrode_probe_channel_map_field(self):
        ntrode_probe_channel_map_fields = self.nwb_metadata.metadata['ntrode probe channel map'][0].keys()
        self.assertIn('map', ntrode_probe_channel_map_fields)
        self.assertIn('probe_id', ntrode_probe_channel_map_fields)
        self.assertIn('ntrode_id', ntrode_probe_channel_map_fields)

