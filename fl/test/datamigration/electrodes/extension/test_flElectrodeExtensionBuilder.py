import os
from unittest import TestCase

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.header.module.header import Header
from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension_builder import \
    FlElectrodeExtensionBuilder

from testfixtures import should_raise

path = os.path.dirname(os.path.abspath(__file__))


class TestFlElectrodeExtensionBuilder(TestCase):

    def test_electrode_extension_builder_build_fl_electrode_extension_successfully(self):
        probes_metadata = [
            {'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1,
             'shanks': [
                 {'shank_id': 0,
                  'electrodes': [
                      {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                      {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}
                  ]}
             ]},
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
                     {'id': 97, 'rel_x': 40, 'rel_y': 900, 'rel_z': 0}
                 ]}
             ]}
        ]

        electrode_groups_metadata = [
            {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'},
            {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'}]

        ntrode_metadata = [
            {'ntrode_id': 1, 'probe_id': 0, 'bad_channels': [0, 2], 'map': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}},
            {'ntrode_id': 2, 'probe_id': 0, 'bad_channels': [0, 3], 'map': {0: 32, 1: 33, 2: 34, 3: 35, 4: 36}},
            {'ntrode_id': 3, 'probe_id': 1, 'bad_channels': [0, 1], 'map': {0: 64, 1: 65, 2: 66, 3: 67, 4: 68}},
            {'ntrode_id': 4, 'probe_id': 1, 'bad_channels': [0, 2, 3], 'map': {0: 96, 1: 97, 2: 98, 3: 99, 4: 100}}
        ]
        header = Header(str(path) + '/../../res/nwb_elements_builder_test/header.xml')

        fl_electrode_extension_builder = FlElectrodeExtensionBuilder(
            probes_metadata=probes_metadata,
            electrode_groups_metadata=electrode_groups_metadata,
            ntrode_metadata=ntrode_metadata,
            header=header,
        )
        fl_electrode_extension = fl_electrode_extension_builder.build()

        self.assertEqual(fl_electrode_extension.rel_x, [0, 0, 0, 0, 0, 40, 0, 40, 0, 40, 0, 40])
        self.assertEqual(fl_electrode_extension.rel_y, [0, 0, 0, 0, 0, 0, 300, 300, 600, 600, 900, 900])
        self.assertEqual(fl_electrode_extension.rel_z, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(fl_electrode_extension.hw_chan[0], 81)
        self.assertEqual(fl_electrode_extension.hw_chan[-1], 175)
        self.assertEqual(fl_electrode_extension.ntrode_id, [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4])
        self.assertEqual(
            fl_electrode_extension.bad_channels,
            [
                True, False, True, False, False, True, False, False, True, False, True, True, False, False, False, True,
                False, True, True, False
            ]
        )

    @should_raise(NoneParamException)
    def test_electrode_extension_builder_failed_build_fl_electrode_extension_due_to_None_param(self):
        fl_electrode_extension_builder = FlElectrodeExtensionBuilder(
            probes_metadata=None,
            electrode_groups_metadata=None,
            ntrode_metadata=None,
            header=None,
        )
        fl_electrode_extension_builder.build()
