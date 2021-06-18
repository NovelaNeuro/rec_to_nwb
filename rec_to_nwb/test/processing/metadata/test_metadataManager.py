import os
from unittest import TestCase

from testfixtures import should_raise

from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager

path = os.path.dirname(os.path.abspath(__file__))


class TestMetadataManager(TestCase):

    def test_metadata_manager_reading_metadata_successfully(self):
        nwb_metadata = MetadataManager(
            metadata_path=str(path) + '/../res/metadata.yml',
            probes_paths=[
                str(path) + '/../res/probe1.yml',
                str(path) + '/../res/probe2.yml',
                str(path) + '/../res/probe3.yml'
            ]
        )

        metadata_fields = nwb_metadata.metadata.keys()
        self.assertIn('experimenter_name', metadata_fields)
        self.assertIn('lab', metadata_fields)
        self.assertIn('institution', metadata_fields)
        self.assertIn('session_id', metadata_fields)
        self.assertIn('experiment description', metadata_fields)
        self.assertIn('session description', metadata_fields)
        self.assertIn('subject', metadata_fields)
        self.assertIn('tasks', metadata_fields)
        self.assertIn('behavioral_events', metadata_fields)
        self.assertIn('electrode groups', metadata_fields)
        self.assertIn('ntrode electrode group channel map', metadata_fields)

        self.assertIn('units', metadata_fields)
        self.assertIn('unspecified', nwb_metadata.metadata['units']['analog'])
        self.assertIn('unspecified', nwb_metadata.metadata['units']['behavioral_events'])

        subject_fields = nwb_metadata.metadata['subject'].keys()
        self.assertIn('description', subject_fields)
        self.assertIn('genotype', subject_fields)
        self.assertIn('sex', subject_fields)
        self.assertIn('species', subject_fields)
        self.assertIn('subject id', subject_fields)
        self.assertIn('weight', subject_fields)

        tasks_fields = nwb_metadata.metadata['tasks'][0].keys()
        self.assertIn('task_description', tasks_fields)
        self.assertIn('task_name', tasks_fields)

        behavioral_event_fields = nwb_metadata.metadata['behavioral_events'][0].keys()
        self.assertIn('description', behavioral_event_fields)
        self.assertIn('name', behavioral_event_fields)

        electrode_groups_fields = nwb_metadata.metadata['electrode groups'][0].keys()
        self.assertIn('id', electrode_groups_fields)
        self.assertIn('location', electrode_groups_fields)
        self.assertIn('device_type', electrode_groups_fields)
        self.assertIn('description', electrode_groups_fields)

        ntrode_probe_channel_map_fields = nwb_metadata.metadata['ntrode electrode group channel map'][0].keys()
        self.assertIn('map', ntrode_probe_channel_map_fields)
        self.assertIn('electrode_group_id', ntrode_probe_channel_map_fields)
        self.assertIn('ntrode_id', ntrode_probe_channel_map_fields)

    def test_metadata_manager_reading_probes_successfully(self):
        nwb_metadata = MetadataManager(
            metadata_path=str(path) + '/../res/metadata.yml',
            probes_paths=[
                str(path) + '/../res/probe1.yml',
                str(path) + '/../res/probe2.yml',
                str(path) + '/../res/probe3.yml'
            ]
        )

        shanks_fields = nwb_metadata.probes[0]['shanks'][0].keys()
        self.assertIn('shank_id', shanks_fields)
        self.assertIn('electrodes', shanks_fields)
        self.assertIn('electrodes', shanks_fields)

        self.assertEqual(nwb_metadata.probes[0]['probe_type'], 'tetrode_12.5')
        self.assertEqual(nwb_metadata.probes[0]['probe_description'], 'four wire electrode')
        self.assertEqual(nwb_metadata.probes[0]['contact_side_numbering'], True)
        self.assertEqual(nwb_metadata.probes[0]['contact_size'], 12.5)

    @should_raise(TypeError)
    def test_metadata_manager_failed_reading_metadata_due_to_None_param(self):
        MetadataManager(
            metadata_path=None,
            probes_paths=[
                str(path) + '/res/probe1.yml',
                str(path) + '/res/probe2.yml',
                str(path) + '/res/probe3.yml'
            ]
        )

    @should_raise(TypeError)
    def test_metadata_manager_failed_reading_metadata_due_to_incorrect_type_of_param(self):
        MetadataManager(
            metadata_path=123,
            probes_paths=[
                str(path) + '/res/probe1.yml',
                str(path) + '/res/probe2.yml',
                str(path) + '/res/probe3.yml'
            ]
        )
