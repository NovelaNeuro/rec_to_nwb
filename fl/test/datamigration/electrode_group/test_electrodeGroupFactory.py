from unittest import TestCase
from unittest.mock import Mock

from ndx_fllab_novela.probe import Probe
from pynwb.device import Device
from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.electrode_group.electrode_group_factory import ElectrodeGroupFactory
from fl.datamigration.nwb.components.electrode_group.fl_nwb_electrode_group import FlNwbElectrodeGroup


class TestElectrodeGroupFactory(TestCase):

    def test_creator_create_NwbElectrodeGroup_successfully(self):
        mock_probe = Mock(spec=Probe)
        mock_device = Mock(spec=Device)

        mock_fl_nwb_electrode_group_1 = Mock(spec=FlNwbElectrodeGroup)
        mock_fl_nwb_electrode_group_1.device = mock_probe
        mock_fl_nwb_electrode_group_1.metadata = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                                     'description': 'ElectrodeGroup 1'}

        mock_fl_nwb_electrode_group_2 = Mock(spec=FlNwbElectrodeGroup)
        mock_fl_nwb_electrode_group_2.device = mock_device
        mock_fl_nwb_electrode_group_2.metadata = {'id': 1, 'location': 'mPFC',
                                                     'device_type': '128c-4s8mm6cm-20um-40um-sl',
                                                     'description': 'ElectrodeGroup 2'}

        nwb_electrode_group_1 = ElectrodeGroupFactory.create_nwb_electrode_group(mock_fl_nwb_electrode_group_1)
        nwb_electrode_group_2 = ElectrodeGroupFactory.create_nwb_electrode_group(mock_fl_nwb_electrode_group_2)
        
        self.assertIsNotNone(nwb_electrode_group_1)
        self.assertIsNotNone(nwb_electrode_group_2)

        self.assertEqual(nwb_electrode_group_1.name, 'electrode group 0')
        self.assertEqual(nwb_electrode_group_1.location, 'mPFC')
        self.assertEqual(nwb_electrode_group_1.description, 'ElectrodeGroup 1')
        self.assertEqual(nwb_electrode_group_1.id, 0)
        self.assertEqual(nwb_electrode_group_1.device, mock_probe)

        self.assertEqual(nwb_electrode_group_2.name, 'electrode group 1')
        self.assertEqual(nwb_electrode_group_2.location, 'mPFC')
        self.assertEqual(nwb_electrode_group_2.description, 'ElectrodeGroup 2')
        self.assertEqual(nwb_electrode_group_2.id, 1)
        self.assertEqual(nwb_electrode_group_2.device, mock_device)

    @should_raise(NoneParamException)
    def test_creator_failed_creating_ElectrodeGroup_due_to_lack_of_NwbElectrodeGroup(self):
        ElectrodeGroupFactory.create_nwb_electrode_group(None)

    @should_raise(NoneParamException)
    def test_creator_failed_creating_ElectrodeGroup_due_to_lack_of_NwbElectrodeGroup_attr(self):
        mock_fl_nwb_electrode_group_1 = Mock(spec=FlNwbElectrodeGroup)
        mock_fl_nwb_electrode_group_1.device = None
        mock_fl_nwb_electrode_group_1.metadata = {'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5',
                                                 'description': 'ElectrodeGroup 1'}

        ElectrodeGroupFactory.create_nwb_electrode_group(mock_fl_nwb_electrode_group_1)