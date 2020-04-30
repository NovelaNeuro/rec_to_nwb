import os
from unittest import TestCase
from unittest.mock import Mock

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.electrode_group.fl_electrode_group_manager import FlElectrodeGroupManager
from fl.datamigration.nwb.components.electrode_group.fl_electrode_group import FlElectrodeGroup

from ndx_fl_novela.probe import Probe
from testfixtures import should_raise


path = os.path.dirname(os.path.abspath(__file__))


class TestFlElectrodeGroupManager(TestCase):

    def test_manager_builds_FlElectrodeGroups_successfully(self):
        electrode_groups_metadata_1 = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                           'description': 'Probe 1'}
        electrode_groups_metadata_2 = {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl',
                                           'description': 'Probe 2'}
        electrode_groups_metadata = [electrode_groups_metadata_1, electrode_groups_metadata_2]

        mock_probe_1 = Mock(spec=Probe)
        mock_probe_1.probe_type = 'tetrode_12.5'
        mock_probe_2 = Mock(spec=Probe)
        mock_probe_2.probe_type = '128c-4s8mm6cm-20um-40um-sl'
        probes = [mock_probe_1, mock_probe_2]

        fl_electrode_group_manager = FlElectrodeGroupManager(
            electrode_groups_metadata=electrode_groups_metadata
        )

        fl_electrode_groups = fl_electrode_group_manager.get_fl_electrode_groups(
            probes=probes
        )
        self.assertEqual(2, len(fl_electrode_groups))
        self.assertIsInstance(fl_electrode_groups, list)

        self.assertIsInstance(fl_electrode_groups[0], FlElectrodeGroup)
        self.assertEqual(fl_electrode_groups[0].metadata, electrode_groups_metadata_1)
        self.assertEqual(fl_electrode_groups[0].device, mock_probe_1)

        self.assertIsInstance(fl_electrode_groups[1], FlElectrodeGroup)
        self.assertEqual(fl_electrode_groups[1].metadata, electrode_groups_metadata_2)
        self.assertEqual(fl_electrode_groups[1].device, mock_probe_2)

    @should_raise(NoneParamException)
    def test_manager_failed_builds_FlElectrodeGroups_due_to_None_metadata(self):
        mock_probe_1 = Mock(spec=Probe)
        mock_probe_2 = Mock(spec=Probe)
        probes = [mock_probe_1, mock_probe_2]

        fl_electrode_group_manager = FlElectrodeGroupManager(
            electrode_groups_metadata=None
        )
        fl_electrode_group_manager.get_fl_electrode_groups(
            probes=probes
        )

    @should_raise(NoneParamException)
    def test_manager_failed_builds_FlElectrodeGroups_due_to_None_probes(self):
        electrode_groups_metadata_1 = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                       'description': 'Probe 1'}
        electrode_groups_metadata_2 = {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl',
                                       'description': 'Probe 2'}
        electrode_groups_metadata = [electrode_groups_metadata_1, electrode_groups_metadata_2]

        fl_electrode_group_manager = FlElectrodeGroupManager(
            electrode_groups_metadata=electrode_groups_metadata
        )
        fl_electrode_group_manager.get_fl_electrode_groups(
            probes=None
        )
