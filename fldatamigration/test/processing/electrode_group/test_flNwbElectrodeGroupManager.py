import os
from unittest import TestCase
from unittest.mock import Mock

from fldatamigration.processing.nwb.components.electrode_group.fl_nwb_electrode_group import FlNwbElectrodeGroup
from fldatamigration.processing.nwb.components.electrode_group.fl_nwb_electrode_group_manager import FlNwbElectrodeGroupManager

from ndx_fl_novela.probe import Probe
from testfixtures import should_raise

path = os.path.dirname(os.path.abspath(__file__))


class TestFlNwbElectrodeGroupManager(TestCase):

    def test_fl_nwb_electrode_group_manager_get_FlElectrodeGroups_successfully(self):
        electrode_groups_metadata_1 = {
            'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1',
            'targeted_location': 'Sample predicted location 1', 'targeted_x': 0.0, 'targeted_y': 0.0,
            'targeted_z': 0.0, 'units': 'um'
        }
        electrode_groups_metadata_2 = {
            'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2',
            'targeted_location': 'Sample predicted location 2', 'targeted_x': 0.0, 'targeted_y': 0.0,
            'targeted_z': 0.0, 'units': 'um'
        }
        electrode_groups_metadata_3 = {
            'id': 2, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 3',
            'targeted_location': 'Sample predicted location 3', 'targeted_x': 0.0, 'targeted_y': 0.0,
            'targeted_z': 0.0, 'units': 'um'
        }
        electrode_groups_metadata = [
            electrode_groups_metadata_1, electrode_groups_metadata_2, electrode_groups_metadata_3
        ]

        mock_probe_1 = Mock(spec=Probe)
        mock_probe_1.probe_type = 'tetrode_12.5'
        mock_probe_2 = Mock(spec=Probe)
        mock_probe_2.probe_type = '128c-4s8mm6cm-20um-40um-sl'
        probes = [mock_probe_1, mock_probe_2]

        mock_electrode_groups_valid_map = {0, 2}

        fl_nwb_electrode_group_manager = FlNwbElectrodeGroupManager(
            electrode_groups_metadata=electrode_groups_metadata
        )

        fl_nwb_electrode_groups = fl_nwb_electrode_group_manager.get_fl_nwb_electrode_groups(
            probes=probes,
            electrode_groups_valid_map=mock_electrode_groups_valid_map
        )
        self.assertEqual(2, len(fl_nwb_electrode_groups))
        self.assertIsInstance(fl_nwb_electrode_groups, list)

        self.assertIsInstance(fl_nwb_electrode_groups[0], FlNwbElectrodeGroup)
        self.assertEqual(fl_nwb_electrode_groups[0].name, 'electrode group 0')
        self.assertEqual(fl_nwb_electrode_groups[0].description, 'Probe 1')
        self.assertEqual(fl_nwb_electrode_groups[0].location, 'mPFC')
        self.assertEqual(fl_nwb_electrode_groups[0].device, mock_probe_1)
        self.assertEqual(fl_nwb_electrode_groups[0].targeted_location, 'Sample predicted location 1')
        self.assertEqual(fl_nwb_electrode_groups[0].targeted_x, 0.0)
        self.assertEqual(fl_nwb_electrode_groups[0].targeted_y, 0.0)
        self.assertEqual(fl_nwb_electrode_groups[0].targeted_z, 0.0)
        self.assertEqual(fl_nwb_electrode_groups[0].units, 'um')

        self.assertIsInstance(fl_nwb_electrode_groups[1], FlNwbElectrodeGroup)
        self.assertEqual(fl_nwb_electrode_groups[1].name, 'electrode group 2')
        self.assertEqual(fl_nwb_electrode_groups[1].description, 'Probe 3')
        self.assertEqual(fl_nwb_electrode_groups[1].location, 'mPFC')
        self.assertEqual(fl_nwb_electrode_groups[1].device, mock_probe_2)
        self.assertEqual(fl_nwb_electrode_groups[1].targeted_location, 'Sample predicted location 3')
        self.assertEqual(fl_nwb_electrode_groups[1].targeted_x, 0.0)
        self.assertEqual(fl_nwb_electrode_groups[1].targeted_y, 0.0)
        self.assertEqual(fl_nwb_electrode_groups[1].targeted_z, 0.0)
        self.assertEqual(fl_nwb_electrode_groups[1].units, 'um')

    @should_raise(TypeError)
    def test_fl_nwb_electrode_group_manager_failed_init_due_to_None_metadata(self):
        FlNwbElectrodeGroupManager(
            electrode_groups_metadata=None
        )

    @should_raise(TypeError)
    def test_fl_nwb_electrode_group_manager_failed_get_FlNwbElectrodeGroups_due_to_None_params(self):
        fl_nwb_electrode_group_manager = FlNwbElectrodeGroupManager(
            electrode_groups_metadata=[{}, {}]
        )
        fl_nwb_electrode_group_manager.get_fl_nwb_electrode_groups(
            probes=None,
            electrode_groups_valid_map=None
        )
