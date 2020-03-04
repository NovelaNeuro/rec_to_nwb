import os
from unittest import TestCase
from unittest.mock import Mock

from ndx_lflab_novela.fl_electrode_group import FLElectrodeGroup
from ndx_lflab_novela.probe import Probe
from testfixtures import should_raise

from src.datamigration.exceptions.none_param_in_init_exception import NoneParamInInitException
from src.datamigration.nwb.components.electrode_group.lf_electrode_group_manager import FlElectrodeGroupManager
from src.datamigration.nwb.components.electrode_group.lf_fl_electrode_group import LfFLElectrodeGroup

path = os.path.dirname(os.path.abspath(__file__))


class TestFlElectrodeGroupManager(TestCase):

    def test_manager_builds_LfFLElectrodeGroups_successfully(self):
        electrode_groups_metadata_1 = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                           'description': 'Probe 1'}
        electrode_groups_metadata_2 = {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl',
                                           'description': 'Probe 2'}
        electrode_groups_metadata = [electrode_groups_metadata_1, electrode_groups_metadata_2]

        mock_probe_1 = Mock(spec=Probe)
        mock_probe_2 = Mock(spec=Probe)
        probes = [mock_probe_1, mock_probe_2]

        fl_electrode_group_manager = FlElectrodeGroupManager(
            electrode_groups_metadata=electrode_groups_metadata
        )

        lf_fl_electrode_groups = fl_electrode_group_manager.get_lf_fl_electrode_groups(
            probes=probes
        )
        self.assertEqual(2, len(lf_fl_electrode_groups))
        self.assertIsInstance(lf_fl_electrode_groups, list)

        self.assertIsInstance(lf_fl_electrode_groups[0], LfFLElectrodeGroup)
        self.assertEqual(lf_fl_electrode_groups[0].metadata, electrode_groups_metadata_1)
        self.assertEqual(lf_fl_electrode_groups[0].device, mock_probe_1)

        self.assertIsInstance(lf_fl_electrode_groups[1], LfFLElectrodeGroup)
        self.assertEqual(lf_fl_electrode_groups[1].metadata, electrode_groups_metadata_2)
        self.assertEqual(lf_fl_electrode_groups[1].device, mock_probe_2)

    @should_raise(NoneParamInInitException)
    def test_manager_failed_builds_LfFLElectrodeGroups_due_to_None_metadata(self):
        mock_probe_1 = Mock(spec=Probe)
        mock_probe_2 = Mock(spec=Probe)
        probes = [mock_probe_1, mock_probe_2]

        fl_electrode_group_manager = FlElectrodeGroupManager(
            electrode_groups_metadata=None
        )
        fl_electrode_group_manager.get_lf_fl_electrode_groups(
            probes=probes
        )

    @should_raise(NoneParamInInitException)
    def test_manager_failed_builds_LfFLElectrodeGroups_due_to_None_probes(self):
        electrode_groups_metadata_1 = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                       'description': 'Probe 1'}
        electrode_groups_metadata_2 = {'id': 1, 'location': 'mPFC', 'device_type': '128c-4s8mm6cm-20um-40um-sl',
                                       'description': 'Probe 2'}
        electrode_groups_metadata = [electrode_groups_metadata_1, electrode_groups_metadata_2]

        fl_electrode_group_manager = FlElectrodeGroupManager(
            electrode_groups_metadata=electrode_groups_metadata
        )
        fl_electrode_group_manager.get_lf_fl_electrode_groups(
            probes=None
        )
