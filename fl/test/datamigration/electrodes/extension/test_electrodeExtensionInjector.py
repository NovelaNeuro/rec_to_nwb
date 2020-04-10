import unittest
from datetime import datetime
from unittest.mock import Mock

from fl.datamigration.exceptions.none_param_exception import NoneParamException

from fl.datamigration.exceptions.not_compatible_metadata import NotCompatibleMetadata
from fl.datamigration.nwb.components.electrodes.electrode_creator import ElectrodesCreator
from fl.datamigration.nwb.components.electrodes.extension.electrode_extension_injector import ElectrodeExtensionInjector
from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension import FlElectrodeExtension
from fl.datamigration.nwb.components.electrodes.fl_electrode_manager import FlElectrodeManager

from dateutil.tz import tzlocal
from hdmf.common import VectorData
from ndx_fllab_novela.nwb_electrode_group import NwbElectrodeGroup
from pynwb import NWBFile
from testfixtures import should_raise



class TestElectrodeExtensionInjector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.metadata = [{'id': 0, 'location': 'mPFC', 'device_type': 'tetrode_12.5', 'description': 'Probe 1'}]

        cls.probes = [{'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'num_shanks': 1, 'shanks': [
            {'shank_id': 0,
             'electrodes': [
                 {'id': 0, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                 {'id': 1, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                 {'id': 2, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0},
                 {'id': 3, 'rel_x': 0, 'rel_y': 0, 'rel_z': 0}]}]}]


        cls.mock_eg_1 = Mock(spec=NwbElectrodeGroup)
        cls.mock_eg_2 = Mock(spec=NwbElectrodeGroup)
        cls.mock_eg_1.name = 'NwbElectrodeGroup1'
        cls.mock_eg_2.name = 'NwbElectrodeGroup2'
        cls.electrode_groups = [cls.mock_eg_1, cls.mock_eg_2]

    def setUp(self):
        self.nwb_file = NWBFile(
            session_description='None',
            identifier='NWB1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        self.electrode_extension_injector = ElectrodeExtensionInjector()
        self.fl_electrodes_manager = FlElectrodeManager(self.probes, self.metadata)

        fl_electrodes = self.fl_electrodes_manager.get_fl_electrodes(
            electrode_groups=self.electrode_groups,
        )

        self.electrode_creator = ElectrodesCreator()
        [self.electrode_creator.create(self.nwb_file, fl_electrode) for fl_electrode in fl_electrodes]

    def test_electrode_extension_injector_inject_proper_values_successfully(self):
        mock_fl_electrode_extension = Mock(spec=FlElectrodeExtension)
        mock_fl_electrode_extension.rel_x = [0, 0, 0, 0]
        mock_fl_electrode_extension.rel_y = [1, 1, 1, 1]
        mock_fl_electrode_extension.rel_z = [2, 2, 2, 2]
        mock_fl_electrode_extension.hw_chan = [0, 1, 2, 3]
        mock_fl_electrode_extension.ntrode_id = [11, 11, 22, 22]
        mock_fl_electrode_extension.bad_channels = [True, False, False, True]
        mock_fl_electrode_extension.probe_shank = [0, 0, 1, 2]

        self.electrode_extension_injector.inject_extensions(
            nwb_content=self.nwb_file,
            fl_electrode_extension=mock_fl_electrode_extension
        )

        self.assertIsInstance(self.nwb_file.electrodes['rel_x'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['rel_y'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['rel_z'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['ntrode_id'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['bad_channels'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['hwChan'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['probe_shank'], VectorData)

        # header_extension - hw_chan
        self.assertIsInstance(self.nwb_file.electrodes[0, 9], int)
        self.assertEqual(self.nwb_file.electrodes[0, 9], 0)
        self.assertEqual(self.nwb_file.electrodes[1, 9], 1)
        self.assertEqual(self.nwb_file.electrodes[2, 9], 2)
        self.assertEqual(self.nwb_file.electrodes[3, 9], 3)

        # ntrodes_extension - ntrode_id
        self.assertIsInstance(self.nwb_file.electrodes[0, 10], int)
        self.assertEqual(self.nwb_file.electrodes[0, 10], 11)
        self.assertEqual(self.nwb_file.electrodes[1, 10], 11)
        self.assertEqual(self.nwb_file.electrodes[2, 10], 22)
        self.assertEqual(self.nwb_file.electrodes[3, 10], 22)

        # ntrodes_extension - bad_channels
        self.assertIsInstance(self.nwb_file.electrodes[0, 11], bool)
        self.assertEqual(self.nwb_file.electrodes[0, 11], True)
        self.assertEqual(self.nwb_file.electrodes[1, 11], False)
        self.assertEqual(self.nwb_file.electrodes[2, 11], False)
        self.assertEqual(self.nwb_file.electrodes[3, 11], True)

        # metadata_extension - rel_x
        self.assertIsInstance(self.nwb_file.electrodes[0, 12], int)
        self.assertEqual(self.nwb_file.electrodes[0, 12], 0)
        self.assertEqual(self.nwb_file.electrodes[1, 12], 0)
        self.assertEqual(self.nwb_file.electrodes[2, 12], 0)
        self.assertEqual(self.nwb_file.electrodes[3, 12], 0)

        # metadata_extension - rel_y
        self.assertIsInstance(self.nwb_file.electrodes[0, 13], int)
        self.assertEqual(self.nwb_file.electrodes[0, 13], 1)
        self.assertEqual(self.nwb_file.electrodes[1, 13], 1)
        self.assertEqual(self.nwb_file.electrodes[2, 13], 1)
        self.assertEqual(self.nwb_file.electrodes[3, 13], 1)
        
        # metadata_extension - rel_z
        self.assertIsInstance(self.nwb_file.electrodes[0, 14], int)
        self.assertEqual(self.nwb_file.electrodes[0, 14], 2)
        self.assertEqual(self.nwb_file.electrodes[1, 14], 2)
        self.assertEqual(self.nwb_file.electrodes[2, 14], 2)
        self.assertEqual(self.nwb_file.electrodes[3, 14], 2)

        # metadata_extension - proba_shank
        self.assertIsInstance(self.nwb_file.electrodes[0, 15], int)
        self.assertEqual(self.nwb_file.electrodes[0, 15], 0)
        self.assertEqual(self.nwb_file.electrodes[1, 15], 0)
        self.assertEqual(self.nwb_file.electrodes[2, 15], 1)
        self.assertEqual(self.nwb_file.electrodes[3, 15], 2)

    @should_raise(NotCompatibleMetadata)
    def test_electrodes_extension_injector_failed_injecting_due_to_longer_param(self):

        mock_fl_electrode_extension = Mock(spec=FlElectrodeExtension)
        mock_fl_electrode_extension.rel_x = [0, 0, 0, 0]
        mock_fl_electrode_extension.rel_y = [1, 1, 1, 1]
        mock_fl_electrode_extension.rel_z = [2, 2, 2, 2]
        mock_fl_electrode_extension.hw_chan = [0, 1, 2, 3, 4]
        mock_fl_electrode_extension.ntrode_id = [11, 11, 22, 22]
        mock_fl_electrode_extension.bad_channels = [True, False, False, True]
        mock_fl_electrode_extension.probe_shank = [0, 0, 1, 2]

        self.electrode_extension_injector.inject_extensions(self.nwb_file, mock_fl_electrode_extension)

    @should_raise(NotCompatibleMetadata)
    def test_electrodes_extension_injector_failed_injecting_due_to_shorter_param(self):
        mock_fl_electrode_extension = Mock(spec=FlElectrodeExtension)
        mock_fl_electrode_extension.rel_x = [0, 0, 0]
        mock_fl_electrode_extension.rel_y = [1, 1, 1, 1]
        mock_fl_electrode_extension.rel_z = [2, 2, 2, 2]
        mock_fl_electrode_extension.hw_chan = [0, 1, 2, 3]
        mock_fl_electrode_extension.ntrode_id = [11, 11, 22, 22]
        mock_fl_electrode_extension.bad_channels = [True, False, False, True]
        mock_fl_electrode_extension.probe_shank = [0, 0, 1, 2]

        self.electrode_extension_injector.inject_extensions(self.nwb_file, mock_fl_electrode_extension)

    @should_raise(NoneParamException)
    def test_electrodes_extension_injector_failed_injecting_due_to_None_param(self):
        mock_fl_electrode_extension = Mock(spec=FlElectrodeExtension)
        mock_fl_electrode_extension.rel_x = [0, 0, 0]
        mock_fl_electrode_extension.rel_y = [1, 1, 1, 1]
        mock_fl_electrode_extension.rel_z = [2, 2, 2, 2]
        mock_fl_electrode_extension.hw_chan = [0, 1, 2, 3]
        mock_fl_electrode_extension.ntrode_id = [11, 11, 22, 22]
        mock_fl_electrode_extension.bad_channels = [True, False, False, True]
        mock_fl_electrode_extension.probe_shank = None

        self.electrode_extension_injector.inject_extensions(self.nwb_file, mock_fl_electrode_extension)

