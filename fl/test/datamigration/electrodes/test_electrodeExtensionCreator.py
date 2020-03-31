import os
from unittest import TestCase

from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.header.module.header import Header
from fl.datamigration.nwb.components.electrodes.electrode_extension_creator import ElectrodeExtensionCreator

path = os.path.dirname(os.path.abspath(__file__))


class TestElectrodeExtensionsCreator(TestCase):

    def test_electrode_extension_creator_build_extensions_successfully(self):
        metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}
        ]

        probes = [{'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
                   'shanks': [
                       {'shank_id': 0,
                        'electrodes': [
                            {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                            {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                            {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                            {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]},
                  {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
                   'shanks': [
                       {'shank_id': 0, 'electrodes': [
                           {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                           {'id': 1, 'rel_x': 40, 'rel_y': 0, 'rel_z': 0}]},
                       {'shank_id': 1, 'electrodes': [
                           {'id': 32, 'rel_x': 0, 'rel_y': 300, 'rel_z': 0},
                           {'id': 33, 'rel_x': 40, 'rel_y': 300, 'rel_z': 0}]},
                       {'shank_id': 2, 'electrodes': [
                           {'id': 64, 'rel_x': 0, 'rel_y': 600, 'rel_z': 0},
                           {'id': 65, 'rel_x': 40, 'rel_y': 600, 'rel_z': 0}, ]},
                       {'shank_id': 3, 'electrodes': [
                           {'id': 96, 'rel_x': 0, 'rel_y': 900, 'rel_z': 0},
                           {'id': 97, 'rel_x': 40, 'rel_y': 900, 'rel_z': 0}]}]}
                  ]

        ntrodes_metadata = [
            {'ntrode_id': 1, 'probe_id': 0, 'bad_channels': [0, 2], 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
            {'ntrode_id': 2, 'probe_id': 0, 'bad_channels': [0, 3], 'map': {0: 32, 1: 33, 2: 34, 3: 35, 4: 36}},
            {'ntrode_id': 3, 'probe_id': 1, 'bad_channels': [0, 1], 'map': {0: 64, 1: 65, 2: 66, 3: 67, 4: 68}},
            {'ntrode_id': 4, 'probe_id': 1, 'bad_channels': [0, 2, 3], 'map': {0: 96, 1: 97, 2: 98, 3: 99, 4: 100}}
        ]

        header = Header(str(path) + '/../res/nwb_elements_builder_test/header.xml')

        electrode_extension_creator = ElectrodeExtensionCreator(
            probes_metadata=probes,
            electrode_groups_metadata=metadata,
            header=header,
            ntrodes_metadata=ntrodes_metadata
        )

        electrodes_metadata_extension, electrodes_header_extension, ntrodes_extension_ntrode_id, \
            ntrodes_extension_bad_channels = electrode_extension_creator.create()
        
        self.assertIsNotNone(electrodes_metadata_extension)
        
        self.assertIsNotNone(electrodes_metadata_extension.rel_x)
        self.assertIsNotNone(electrodes_metadata_extension.rel_y)
        self.assertIsNotNone(electrodes_metadata_extension.rel_z)
        self.assertEqual(electrodes_metadata_extension.rel_x[0], 0)
        self.assertEqual(electrodes_metadata_extension.rel_y[0], 0)
        self.assertEqual(electrodes_metadata_extension.rel_z[0], 0)
        
        self.assertIsNotNone(electrodes_header_extension)
        self.assertEqual(electrodes_header_extension[0], '81')

        self.assertIsNotNone(ntrodes_extension_ntrode_id)
        self.assertEqual(ntrodes_extension_ntrode_id[0], 1)
        self.assertEqual(ntrodes_extension_ntrode_id[-1], 4)

        self.assertIsNotNone(ntrodes_extension_bad_channels)
        self.assertEqual(ntrodes_extension_bad_channels[0], True)
        self.assertEqual(ntrodes_extension_bad_channels[-1], False)

    @should_raise(NoneParamException)
    def test_electrode_extension_creator_failed_build_extensions_due_to_None_param(self):
        probes = [{'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
                   'shanks': [
                       {'shank_id': 0,
                        'electrodes': [
                            {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                            {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                            {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                            {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]},
                  {'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'num_shanks': 4,
                   'shanks': [
                       {'shank_id': 0, 'electrodes': [
                           {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                           {'id': 1, 'rel_x': 40, 'rel_y': 0, 'rel_z': 0}]},
                       {'shank_id': 1, 'electrodes': [
                           {'id': 32, 'rel_x': 0, 'rel_y': 300, 'rel_z': 0},
                           {'id': 33, 'rel_x': 40, 'rel_y': 300, 'rel_z': 0}]},
                       {'shank_id': 2, 'electrodes': [
                           {'id': 64, 'rel_x': 0, 'rel_y': 600, 'rel_z': 0},
                           {'id': 65, 'rel_x': 40, 'rel_y': 600, 'rel_z': 0}, ]},
                       {'shank_id': 3, 'electrodes': [
                           {'id': 96, 'rel_x': 0, 'rel_y': 900, 'rel_z': 0},
                           {'id': 97, 'rel_x': 40, 'rel_y': 900, 'rel_z': 0}]}]}
                  ]

        ntrodes_metadata = [
            {'ntrode_id': 1, 'probe_id': 0, 'bad_channels': [0, 2], 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
            {'ntrode_id': 2, 'probe_id': 0, 'bad_channels': [0, 3], 'map': {0: 32, 1: 33, 2: 34, 3: 35, 4: 36}},
            {'ntrode_id': 3, 'probe_id': 1, 'bad_channels': [0, 1], 'map': {0: 64, 1: 65, 2: 66, 3: 67, 4: 68}},
            {'ntrode_id': 4, 'probe_id': 1, 'bad_channels': [0, 2, 3], 'map': {0: 96, 1: 97, 2: 98, 3: 99, 4: 100}}
        ]

        header = Header(str(path) + '/../res/nwb_elements_builder_test/header.xml')

        electrode_extension_creator = ElectrodeExtensionCreator(
            probes_metadata=probes,
            electrode_groups_metadata=None,
            header=header,
            ntrodes_metadata=ntrodes_metadata
        )

        electrode_extension_creator.create()
