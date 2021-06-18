import os
from pathlib import Path
from unittest import TestCase

from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.invalid_header_exception import InvalidHeaderException
from rec_to_nwb.processing.exceptions.invalid_metadata_exception import InvalidMetadataException
from rec_to_nwb.processing.header.module import header
from rec_to_nwb.processing.validation.ntrode_validator import NTrodeValidator

path = os.path.dirname(os.path.abspath(__file__))


class TestNTrodeValidator(TestCase):

    def setUp(self):
        parent_path = str(Path(path).parent)
        res_path = parent_path + '/res/fl_lab_sample_header.xml'
        self.header = header.Header(res_path)

    def test_ntrode_validator_validate_correct_data_successfully(self):
        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 1, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 2, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 3, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0}
                  ]}
             ]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                     {'id': 1, 'rel_x': 40.0, 'rel_y': 0.0, 'rel_z': 0.0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0.0, 'rel_y': 300.0, 'rel_z': 0.0},
                     {'id': 33, 'rel_x': 40.0, 'rel_y': 300.0, 'rel_z': 0.0}]}
             ]}
        ]

        metadata = {
            'electrode_groups': [
                {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
                {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'},
            ],
            "ntrode electrode group channel map": [
                {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
                {"ntrode_id": 2, "electrode_group_id": 1, "bad_channels": [0, 1], "map": {0: 4, 1: 5, 2: 6, 3: 7}},
            ]
        }

        validator = NTrodeValidator(metadata, self.header, probes_metadata)

        result = validator.create_summary()

        self.assertTrue(result.is_valid())

    def test_ntrode_validator_validate_ndtrodes_num_less_than_spikes_successfully(self):
        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 1, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 2, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 3, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0}
                  ]}
             ]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                     {'id': 1, 'rel_x': 40.0, 'rel_y': 0.0, 'rel_z': 0.0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0.0, 'rel_y': 300.0, 'rel_z': 0.0},
                     {'id': 33, 'rel_x': 40.0, 'rel_y': 300.0, 'rel_z': 0.0}]}
             ]}
        ]

        metadata = {
            'electrode_groups': [
                {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            ],
            "ntrode electrode group channel map": [
                {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
            ]
        }

        validator = NTrodeValidator(metadata, self.header, probes_metadata)
        result = validator.create_summary()

        self.assertFalse(result.is_valid())
        self.assertEqual(result.ntrodes_num, 1)

    def test_ntrode_validator_validate_ndtrodes_num_greater_than_spikes_successfully(self):
        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 1, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 2, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 3, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 4, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 5, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 6, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 7, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0}
                  ]}
             ]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                     {'id': 1, 'rel_x': 40.0, 'rel_y': 0.0, 'rel_z': 0.0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0.0, 'rel_y': 300.0, 'rel_z': 0.0},
                     {'id': 33, 'rel_x': 40.0, 'rel_y': 300.0, 'rel_z': 0.0}]}
             ]}
        ]

        metadata = {
            'electrode_groups': [
                {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
                {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'},
            ],
            "ntrode electrode group channel map": [
                {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
                {"ntrode_id": 2, "electrode_group_id": 1, "bad_channels": [0, 1], "map": {0: 4, 1: 5, 2: 6, 3: 7}},
                {"ntrode_id": 3, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 8, 1: 9, 2: 10, 3: 11}},
            ]
        }

        validator = NTrodeValidator(metadata, self.header, probes_metadata)
        result = validator.create_summary()

        self.assertFalse(result.is_valid())
        self.assertEqual(result.ntrodes_num, 3)

    @should_raise(TypeError)
    def test_ntrode_validator_raise_exception_due_to_empty_param(self):
        metadata = {"ntrode electrode group channel map": [
            {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
            {"ntrode_id": 2, "electrode_group_id": 0, "bad_channels": [0, 1], "map": {0: 4, 1: 5, 2: 6, 3: 7}},
            {"ntrode_id": 3, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 8, 1: 9, 2: 10, 3: 11}},
        ]}

        NTrodeValidator(metadata, None, None)

    @should_raise(InvalidHeaderException)
    def test_ntrode_validator_raise_exception_due_to_header_without_spike_ntrodes(self):
        metadata = {"ntrode electrode group channel map": [
            {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
            {"ntrode_id": 2, "electrode_group_id": 0, "bad_channels": [0, 1], "map": {0: 4, 1: 5, 2: 6, 3: 7}},
            {"ntrode_id": 3, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 8, 1: 9, 2: 10, 3: 11}},
        ]}

        validator = NTrodeValidator(metadata, self.header, [])
        self.header.configuration.spike_configuration.spike_n_trodes = None
        validator.create_summary()

    @should_raise(InvalidMetadataException)
    def test_should_raise_exception_due_to_metadata_without_ntrodes(self):
        metadata = {"ntrode electrode group channel map": []}

        validator = NTrodeValidator(metadata, self.header, [])
        validator.create_summary()

    @should_raise(InvalidMetadataException)
    def test_should_raise_exception_due_to_incompatible_probes_metadata_with_ntrodes(self):
        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 1, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 2, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 3, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                      {'id': 5, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0}
                  ]}
             ]},
            {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
             'shanks': [
                 {'shank_id': 0, 'electrodes': [
                     {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                     {'id': 1, 'rel_x': 40.0, 'rel_y': 0.0, 'rel_z': 0.0}]},
                 {'shank_id': 1, 'electrodes': [
                     {'id': 32, 'rel_x': 0.0, 'rel_y': 300.0, 'rel_z': 0.0},
                     {'id': 33, 'rel_x': 40.0, 'rel_y': 300.0, 'rel_z': 0.0}]}
             ]}
        ]

        metadata = {
            'electrode_groups': [
                {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
                {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'},
            ],
            "ntrode electrode group channel map": [
                {"ntrode_id": 1, "electrode_group_id": 0, "bad_channels": [0, 2], "map": {0: 0, 1: 1, 2: 2, 3: 3}},
                {"ntrode_id": 2, "electrode_group_id": 1, "bad_channels": [0, 1], "map": {0: 4, 1: 5, 2: 6, 3: 7}},
            ]
        }

        validator = NTrodeValidator(metadata, self.header, probes_metadata)

        validator.create_summary()

