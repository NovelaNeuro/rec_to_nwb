from unittest import TestCase
from unittest.mock import Mock

from ndx_fllab_novela.probe import Probe
from pynwb.device import Device
from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.electrode_group.fl_electrode_group_creator import FlElectrodeGroupCreator
from fl.datamigration.nwb.components.electrode_group.fl_fl_electrode_group import FlFLElectrodeGroup


class TestFlElectrodeGroupCreator(TestCase):

    def test_creator_create_FLElectrodeGroup_successfully(self):
        mock_probe = Mock(spec=Probe)
        mock_device = Mock(spec=Device)

        mock_fl_fl_electrode_group_1 = Mock(spec=FlFLElectrodeGroup)
        mock_fl_fl_electrode_group_1.device = mock_probe
        mock_fl_fl_electrode_group_1.metadata = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                                     'description': 'ElectrodeGroup 1'}

        mock_fl_fl_electrode_group_2 = Mock(spec=FlFLElectrodeGroup)
        mock_fl_fl_electrode_group_2.device = mock_device
        mock_fl_fl_electrode_group_2.metadata = {'id': 1, 'location': 'mPFC',
                                                     'device_type': '128c-4s8mm6cm-20um-40um-sl',
                                                     'description': 'ElectrodeGroup 2'}

        fl_electrode_group_1 = FlElectrodeGroupCreator.create(mock_fl_fl_electrode_group_1)
        fl_electrode_group_2 = FlElectrodeGroupCreator.create(mock_fl_fl_electrode_group_2)
        
        self.assertIsNotNone(fl_electrode_group_1)
        self.assertIsNotNone(fl_electrode_group_2)

        self.assertEqual(fl_electrode_group_1.name, 'electrode group 0')
        self.assertEqual(fl_electrode_group_1.location, 'mPFC')
        self.assertEqual(fl_electrode_group_1.description, 'ElectrodeGroup 1')
        self.assertEqual(fl_electrode_group_1.id, 0)
        self.assertEqual(fl_electrode_group_1.device, mock_probe)

        self.assertEqual(fl_electrode_group_2.name, 'electrode group 1')
        self.assertEqual(fl_electrode_group_2.location, 'mPFC')
        self.assertEqual(fl_electrode_group_2.description, 'ElectrodeGroup 2')
        self.assertEqual(fl_electrode_group_2.id, 1)
        self.assertEqual(fl_electrode_group_2.device, mock_device)

    @should_raise(NoneParamException)
    def test_creator_failed_creating_ElectrodeGroup_due_to_lack_of_FLElectrodeGroup(self):
        FlElectrodeGroupCreator.create(None)

    @should_raise(NoneParamException)
    def test_creator_failed_creating_ElectrodeGroup_due_to_lack_of_FLElectrodeGroup_attr(self):
        mock_fl_fl_electrode_group_1 = Mock(spec=FlFLElectrodeGroup)
        mock_fl_fl_electrode_group_1.device = None
        mock_fl_fl_electrode_group_1.metadata = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                                 'description': 'ElectrodeGroup 1'}

        FlElectrodeGroupCreator.create(mock_fl_fl_electrode_group_1)