import os
from unittest import TestCase
from unittest.mock import Mock

from fl.datamigration.nwb.components.electrode_group.fl_electrode_group_manager import FlElectrodeGroupManager
from fl.datamigration.nwb.components.electrode_group.fl_electrode_group import FlElectrodeGroup

from ndx_fl_novela.probe import Probe
from testfixtures import should_raise

path = os.path.dirname(os.path.abspath(__file__))


class TestFlElectrodeGroupManager(TestCase):

    def test_fl_electrode_group_manager_get_FlElectrodeGroups_successfully(self):
        electrode_groups_metadata_1 = {
            'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'
        }
        electrode_groups_metadata_2 = {
            'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 2'
        }
        electrode_groups_metadata_3 = {
            'id': 2, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl', 'description': 'Probe 3'
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

        fl_electrode_group_manager = FlElectrodeGroupManager(
            electrode_groups_metadata=electrode_groups_metadata
        )

        fl_electrode_groups = fl_electrode_group_manager.get_fl_electrode_groups(
            probes=probes,
            electrode_groups_valid_map=mock_electrode_groups_valid_map
        )
        self.assertEqual(2, len(fl_electrode_groups))
        self.assertIsInstance(fl_electrode_groups, list)

        self.assertIsInstance(fl_electrode_groups[0], FlElectrodeGroup)
        self.assertEqual(fl_electrode_groups[0].name, 'electrode group 0')
        self.assertEqual(fl_electrode_groups[0].description, 'Probe 1')
        self.assertEqual(fl_electrode_groups[0].location, 'mPFC')
        self.assertEqual(fl_electrode_groups[0].device, mock_probe_1)

        self.assertIsInstance(fl_electrode_groups[1], FlElectrodeGroup)
        self.assertEqual(fl_electrode_groups[1].name, 'electrode group 2')
        self.assertEqual(fl_electrode_groups[1].description, 'Probe 3')
        self.assertEqual(fl_electrode_groups[1].location, 'mPFC')
        self.assertEqual(fl_electrode_groups[1].device, mock_probe_2)

    @should_raise(TypeError)
    def test_fl_electrode_group_manager_failed_init_due_to_None_metadata(self):
        FlElectrodeGroupManager(
            electrode_groups_metadata=None
        )

    @should_raise(TypeError)
    def test_fl_electrode_group_manager_failed_get_FlElectrodeGroups_due_to_None_params(self):
        fl_electrode_group_manager = FlElectrodeGroupManager(
            electrode_groups_metadata=[{}, {}]
        )
        fl_electrode_group_manager.get_fl_electrode_groups(
            probes=None,
            electrode_groups_valid_map=None
        )
