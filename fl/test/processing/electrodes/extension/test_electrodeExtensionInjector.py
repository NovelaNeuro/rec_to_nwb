import unittest
from datetime import datetime
from unittest.mock import Mock

from pynwb.ecephys import ElectrodeGroup

from fldatamigration.processing.exceptions.none_param_exception import NoneParamException

from fldatamigration.processing.exceptions.not_compatible_metadata import NotCompatibleMetadata
from fldatamigration.processing.nwb.components.electrodes.electrode_creator import ElectrodesCreator
from fldatamigration.processing.nwb.components.electrodes.extension.electrode_extension_injector import ElectrodeExtensionInjector
from fldatamigration.processing.nwb.components.electrodes.extension.fl_electrode_extension import FlElectrodeExtension
from fldatamigration.processing.nwb.components.electrodes.fl_electrode_manager import FlElectrodeManager

from dateutil.tz import tzlocal
from hdmf.common import VectorData
from pynwb import NWBFile
from testfixtures import should_raise

from fldatamigration.processing.nwb.components.electrodes.fl_electrodes import FlElectrode


class TestElectrodeExtensionInjector(unittest.TestCase):

    def test_electrode_extension_injector_inject_proper_values_successfully(self):
        mock_eg_1 = Mock(spec=ElectrodeGroup)
        mock_eg_2 = Mock(spec=ElectrodeGroup)
        mock_eg_1.name = 'ElectrodeGroup1'
        mock_eg_2.name = 'ElectrodeGroup2'
        electrode_groups = [mock_eg_1, mock_eg_2]

        nwb_file = NWBFile(
            session_description='None',
            identifier='NWB1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        mock_fl_electrode_0 = Mock(FlElectrode)
        mock_fl_electrode_0.electrode_id = 0
        mock_fl_electrode_0.electrode_group = mock_eg_1

        mock_fl_electrode_1 = Mock(FlElectrode)
        mock_fl_electrode_1.electrode_id = 3
        mock_fl_electrode_1.electrode_group = mock_eg_1

        mock_fl_electrode_2 = Mock(FlElectrode)
        mock_fl_electrode_2.electrode_id = 5
        mock_fl_electrode_2.electrode_group = mock_eg_2

        mock_fl_electrode_3 = Mock(FlElectrode)
        mock_fl_electrode_3.electrode_id = 8
        mock_fl_electrode_3.electrode_group = mock_eg_2
        mock_fl_electrodes = [mock_fl_electrode_0, mock_fl_electrode_1, mock_fl_electrode_2, mock_fl_electrode_3]

        electrode_creator = ElectrodesCreator()
        [electrode_creator.create(nwb_file, fl_electrode) for fl_electrode in mock_fl_electrodes]

        mock_fl_electrode_extension = Mock(spec=FlElectrodeExtension)
        mock_fl_electrode_extension.rel_x = [0, 0, 0, 0]
        mock_fl_electrode_extension.rel_y = [1, 1, 1, 1]
        mock_fl_electrode_extension.rel_z = [2, 2, 2, 2]
        mock_fl_electrode_extension.hw_chan = [0, 1, 2, 3]
        mock_fl_electrode_extension.ntrode_id = [11, 11, 22, 22]
        mock_fl_electrode_extension.bad_channels = [False, False, False, False]
        mock_fl_electrode_extension.probe_shank = [0, 0, 1, 2]
        mock_fl_electrode_extension.probe_channel = [0, 1, 2, 3]

        electrode_extension_injector = ElectrodeExtensionInjector()
        electrode_extension_injector.inject_extensions(
            nwb_content=nwb_file,
            fl_electrode_extension=mock_fl_electrode_extension
        )

        self.assertIsInstance(nwb_file.electrodes['rel_x'], VectorData)
        self.assertIsInstance(nwb_file.electrodes['rel_y'], VectorData)
        self.assertIsInstance(nwb_file.electrodes['rel_z'], VectorData)
        self.assertIsInstance(nwb_file.electrodes['ntrode_id'], VectorData)
        self.assertIsInstance(nwb_file.electrodes['bad_channel'], VectorData)
        self.assertIsInstance(nwb_file.electrodes['hwChan'], VectorData)
        self.assertIsInstance(nwb_file.electrodes['probe_shank'], VectorData)
        self.assertIsInstance(nwb_file.electrodes['probe_channel'], VectorData)

        # header_extension - hw_chan
        self.assertIsInstance(nwb_file.electrodes[0, 9], int)
        self.assertEqual(nwb_file.electrodes[0, 9], 0)
        self.assertEqual(nwb_file.electrodes[1, 9], 1)
        self.assertEqual(nwb_file.electrodes[2, 9], 2)
        self.assertEqual(nwb_file.electrodes[3, 9], 3)

        # ntrodes_extension - ntrode_id
        self.assertIsInstance(nwb_file.electrodes[0, 10], int)
        self.assertEqual(nwb_file.electrodes[0, 10], 11)
        self.assertEqual(nwb_file.electrodes[1, 10], 11)
        self.assertEqual(nwb_file.electrodes[2, 10], 22)
        self.assertEqual(nwb_file.electrodes[3, 10], 22)

        # ntrodes_extension - bad_channels
        self.assertIsInstance(nwb_file.electrodes[0, 11], bool)
        self.assertEqual(nwb_file.electrodes[0, 11], False)
        self.assertEqual(nwb_file.electrodes[1, 11], False)
        self.assertEqual(nwb_file.electrodes[2, 11], False)
        self.assertEqual(nwb_file.electrodes[3, 11], False)

        # metadata_extension - rel_x
        self.assertIsInstance(nwb_file.electrodes[0, 12], int)
        self.assertEqual(nwb_file.electrodes[0, 12], 0)
        self.assertEqual(nwb_file.electrodes[1, 12], 0)
        self.assertEqual(nwb_file.electrodes[2, 12], 0)
        self.assertEqual(nwb_file.electrodes[3, 12], 0)

        # metadata_extension - rel_y
        self.assertIsInstance(nwb_file.electrodes[0, 13], int)
        self.assertEqual(nwb_file.electrodes[0, 13], 1)
        self.assertEqual(nwb_file.electrodes[1, 13], 1)
        self.assertEqual(nwb_file.electrodes[2, 13], 1)
        self.assertEqual(nwb_file.electrodes[3, 13], 1)

        # metadata_extension - rel_z
        self.assertIsInstance(nwb_file.electrodes[0, 14], int)
        self.assertEqual(nwb_file.electrodes[0, 14], 2)
        self.assertEqual(nwb_file.electrodes[1, 14], 2)
        self.assertEqual(nwb_file.electrodes[2, 14], 2)
        self.assertEqual(nwb_file.electrodes[3, 14], 2)

        # metadata_extension - proba_shank
        self.assertIsInstance(nwb_file.electrodes[0, 15], int)
        self.assertEqual(nwb_file.electrodes[0, 15], 0)
        self.assertEqual(nwb_file.electrodes[1, 15], 0)
        self.assertEqual(nwb_file.electrodes[2, 15], 1)
        self.assertEqual(nwb_file.electrodes[3, 15], 2)

        # metadata_extension - probe_channel
        self.assertIsInstance(nwb_file.electrodes[0, 16], int)
        self.assertEqual(nwb_file.electrodes[0, 16], 0)
        self.assertEqual(nwb_file.electrodes[1, 16], 1)
        self.assertEqual(nwb_file.electrodes[2, 16], 2)
        self.assertEqual(nwb_file.electrodes[3, 16], 3)

    @should_raise(NoneParamException)
    def test_electrodes_extension_injector_failed_injecting_due_to_None_fl_electrode_attr(self):
        nwb_file = NWBFile(
            session_description='None',
            identifier='NWB1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )
        mock_fl_electrode_extension = Mock(spec=FlElectrodeExtension)
        mock_fl_electrode_extension.rel_x = [0, 0, 0, 0]
        mock_fl_electrode_extension.rel_y = [1, 1, 1, 1]
        mock_fl_electrode_extension.rel_z = [2, 2, 2, 2]
        mock_fl_electrode_extension.hw_chan = [0, 1, 2, 3]
        mock_fl_electrode_extension.ntrode_id = [11, 11, 22, 22]
        mock_fl_electrode_extension.bad_channels = [False, False, False, False]
        mock_fl_electrode_extension.probe_shank = None
        mock_fl_electrode_extension.probe_channel = [0, 1, 2, 3]

        electrode_extension_injector = ElectrodeExtensionInjector()
        electrode_extension_injector.inject_extensions(
            nwb_content=nwb_file,
            fl_electrode_extension=mock_fl_electrode_extension
        )

    @should_raise(TypeError)
    def test_electrodes_extension_injector_failed_init_due_to_None_param(self):
        ElectrodeExtensionInjector.inject_extensions(None, None)
