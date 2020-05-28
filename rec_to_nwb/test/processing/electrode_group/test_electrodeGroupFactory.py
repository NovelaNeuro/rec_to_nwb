from unittest import TestCase
from unittest.mock import Mock

from rec_to_nwb.processing.exceptions.none_param_exception import NoneParamException
from rec_to_nwb.processing.nwb.components.electrode_group.electrode_group_factory import ElectrodeGroupFactory
from rec_to_nwb.processing.nwb.components.electrode_group.fl_electrode_group import FlElectrodeGroup
from rec_to_nwb.processing.nwb.components.electrode_group.fl_nwb_electrode_group import FlNwbElectrodeGroup

from ndx_franklab_novela.probe import Probe
from pynwb.device import Device
from testfixtures import should_raise


class TestElectrodeGroupFactory(TestCase):

    def test_electrode_group_factory_create_ElectrodeGroup_successfully(self):
        mock_probe = Mock(spec=Probe)
        mock_device = Mock(spec=Device)

        mock_fl_electrode_group_1 = Mock(spec=FlElectrodeGroup)
        mock_fl_electrode_group_1.name = '0'
        mock_fl_electrode_group_1.description = 'ElectrodeGroup 1'
        mock_fl_electrode_group_1.location = 'mPFC'
        mock_fl_electrode_group_1.device = mock_probe

        mock_fl_electrode_group_2 = Mock(spec=FlElectrodeGroup)
        mock_fl_electrode_group_2.name = '1'
        mock_fl_electrode_group_2.description = 'ElectrodeGroup 2'
        mock_fl_electrode_group_2.location = 'mPFC'
        mock_fl_electrode_group_2.device = mock_device

        electrode_group_1 = ElectrodeGroupFactory.create_electrode_group(mock_fl_electrode_group_1)
        electrode_group_2 = ElectrodeGroupFactory.create_electrode_group(mock_fl_electrode_group_2)
        
        self.assertIsNotNone(electrode_group_1)
        self.assertIsNotNone(electrode_group_2)
        self.assertEqual(electrode_group_1.name, "0")
        self.assertEqual(electrode_group_1.description, 'ElectrodeGroup 1')
        self.assertEqual(electrode_group_1.location, 'mPFC')
        self.assertEqual(electrode_group_1.device, mock_probe)
        self.assertEqual(electrode_group_2.name, '1')
        self.assertEqual(electrode_group_2.description, 'ElectrodeGroup 2')
        self.assertEqual(electrode_group_2.location, 'mPFC')
        self.assertEqual(electrode_group_2.device, mock_device)

    def test_electrode_group_factory_create_NwbElectrodeGroup_successfully(self):
        mock_probe = Mock(spec=Probe)
        mock_device = Mock(spec=Device)

        mock_fl_nwb_electrode_group_1 = Mock(spec=FlNwbElectrodeGroup)
        mock_fl_nwb_electrode_group_1.name = '0'
        mock_fl_nwb_electrode_group_1.description = 'ElectrodeGroup 1'
        mock_fl_nwb_electrode_group_1.location = 'mPFC'
        mock_fl_nwb_electrode_group_1.device = mock_probe
        mock_fl_nwb_electrode_group_1.targeted_location = 'Sample location'
        mock_fl_nwb_electrode_group_1.targeted_x = 0.0
        mock_fl_nwb_electrode_group_1.targeted_y = 0.0
        mock_fl_nwb_electrode_group_1.targeted_z = 0.0
        mock_fl_nwb_electrode_group_1.units = 'um'

        mock_fl_nwb_electrode_group_2 = Mock(spec=FlNwbElectrodeGroup)
        mock_fl_nwb_electrode_group_2.name = '1'
        mock_fl_nwb_electrode_group_2.description = 'ElectrodeGroup 2'
        mock_fl_nwb_electrode_group_2.location = 'mPFC'
        mock_fl_nwb_electrode_group_2.device = mock_device
        mock_fl_nwb_electrode_group_2.targeted_location = 'Sample location'
        mock_fl_nwb_electrode_group_2.targeted_x = 0.0
        mock_fl_nwb_electrode_group_2.targeted_y = 0.0
        mock_fl_nwb_electrode_group_2.targeted_z = 0.0
        mock_fl_nwb_electrode_group_2.units = 'mm'

        nwb_electrode_group_1 = ElectrodeGroupFactory.create_nwb_electrode_group(mock_fl_nwb_electrode_group_1)
        nwb_electrode_group_2 = ElectrodeGroupFactory.create_nwb_electrode_group(mock_fl_nwb_electrode_group_2)

        self.assertIsNotNone(nwb_electrode_group_1)
        self.assertIsNotNone(nwb_electrode_group_2)
        self.assertEqual(nwb_electrode_group_1.name, "0")
        self.assertEqual(nwb_electrode_group_1.description, 'ElectrodeGroup 1')
        self.assertEqual(nwb_electrode_group_1.location, 'mPFC')
        self.assertEqual(nwb_electrode_group_1.device, mock_probe)
        self.assertEqual(nwb_electrode_group_1.targeted_location, 'Sample location')
        self.assertEqual(nwb_electrode_group_1.targeted_x, 0.0)
        self.assertEqual(nwb_electrode_group_1.targeted_y, 0.0)
        self.assertEqual(nwb_electrode_group_1.targeted_z, 0.0)
        self.assertEqual(nwb_electrode_group_1.units, 'um')

        self.assertEqual(nwb_electrode_group_2.name, '1')
        self.assertEqual(nwb_electrode_group_2.description, 'ElectrodeGroup 2')
        self.assertEqual(nwb_electrode_group_2.location, 'mPFC')
        self.assertEqual(nwb_electrode_group_2.device, mock_device)
        self.assertEqual(nwb_electrode_group_2.targeted_location, 'Sample location')
        self.assertEqual(nwb_electrode_group_2.targeted_x, 0.0)
        self.assertEqual(nwb_electrode_group_2.targeted_y, 0.0)
        self.assertEqual(nwb_electrode_group_2.targeted_z, 0.0)
        self.assertEqual(nwb_electrode_group_2.units, 'mm')

    @should_raise(TypeError)
    def test_electrode_group_factory_failed_creating_ElectrodeGroup_due_to_lack_of_FLElectrodeGroup(self):
        ElectrodeGroupFactory.create_electrode_group(None)

    @should_raise(NoneParamException)
    def test_electrode_group_factory_failed_creating_ElectrodeGroup_due_to_lack_of_FlElectrodeGroup_attr(self):
        mock_fl_electrode_group_1 = Mock(spec=FlElectrodeGroup)
        mock_fl_electrode_group_1.name = 'ElectrodeGroup 1'
        mock_fl_electrode_group_1.description = 'sample desciption 1'
        mock_fl_electrode_group_1.location = 'sample location 1'
        mock_fl_electrode_group_1.device = None

        ElectrodeGroupFactory.create_electrode_group(mock_fl_electrode_group_1)

    @should_raise(TypeError)
    def test_electrode_group_factory_failed_creating_NwbElectrodeGroup_due_to_lack_of_FLNwbElectrodeGroup(self):
        ElectrodeGroupFactory.create_nwb_electrode_group(None)

    @should_raise(NoneParamException)
    def test_electrode_group_factory_failed_creating_NwbElectrodeGroup_due_to_lack_of_FlNwbElectrodeGroup_attr(self):
        mock_fl_nwb_electrode_group_1 = Mock(spec=FlNwbElectrodeGroup)
        mock_fl_nwb_electrode_group_1.name = 'ElectrodeGroup 1'
        mock_fl_nwb_electrode_group_1.description = 'sample desciption 1'
        mock_fl_nwb_electrode_group_1.location = 'sample location 1'
        mock_fl_nwb_electrode_group_1.device = None
        mock_fl_nwb_electrode_group_1.targeted_location = None
        mock_fl_nwb_electrode_group_1.targeted_x = None
        mock_fl_nwb_electrode_group_1.targeted_y = None
        mock_fl_nwb_electrode_group_1.targeted_z = None
        mock_fl_nwb_electrode_group_1.units = None

        ElectrodeGroupFactory.create_nwb_electrode_group(mock_fl_nwb_electrode_group_1)