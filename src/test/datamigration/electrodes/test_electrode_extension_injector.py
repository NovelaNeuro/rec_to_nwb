import unittest
from datetime import datetime
from unittest.mock import Mock

from dateutil.tz import tzlocal
from hdmf.common import VectorData
from ndx_franklab_novela.fl_electrode_group import FLElectrodeGroup
from pynwb import NWBFile

from src.datamigration.exceptions.not_compatible_metadata import NotCompatibleMetadata
from src.datamigration.nwb.components.electrodes.electrode_builder import ElectrodeBuilder
from src.datamigration.nwb.components.electrodes.electrode_extension_injector import ElectrodeExtensionInjector
from src.datamigration.nwb.components.electrodes.electrode_metadata_extension_creator import \
    ElectrodesMetadataExtensionCreator


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

        cls.mock_electrodes_metadata_extension = Mock()
        cls.mock_electrodes_metadata_extension.__class__ = ElectrodesMetadataExtensionCreator
        cls.mock_electrodes_metadata_extension.rel_x = [0, 0, 0, 0]
        cls.mock_electrodes_metadata_extension.rel_y = [1, 1, 1, 1]
        cls.mock_electrodes_metadata_extension.rel_z = [2, 2, 2, 2]

        cls.mock_eg_1 = Mock()
        cls.mock_eg_2 = Mock()
        cls.mock_eg_1.__class__ = FLElectrodeGroup
        cls.mock_eg_2.__class__ = FLElectrodeGroup
        cls.mock_eg_1.name = 'FLElectrodeGroup1'
        cls.mock_eg_2.name = 'FLElectrodeGroup2'
        cls.electrode_group_object_dict = {0: cls.mock_eg_1, 1: cls.mock_eg_2}

    def setUp(self):
        self.electrode_extension_injector = ElectrodeExtensionInjector()
        self.electrodes_builder = ElectrodeBuilder(self.probes, self.metadata)

        self.nwb_file = NWBFile(
            session_description='None',
            identifier='NWB1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        self.electrodes_builder.build(
            nwb_content=self.nwb_file,
            electrode_group_dict=self.electrode_group_object_dict,
        )

    def test_injectExtensions_correctReturnType_true(self):
        header_extension = [0, 1, 2, 3]
        ntrodes_extension = [11, 11, 22, 22]

        self.electrode_extension_injector.inject_extensions(
            nwb_content=self.nwb_file,
            metadata_extension=self.mock_electrodes_metadata_extension,
            header_extension=header_extension,
            ntrodes_extension=ntrodes_extension
        )

        self.assertIsInstance(self.nwb_file.electrodes['rel_x'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['rel_y'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['rel_z'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['hwChan'], VectorData)

        # header_extension - hw_chan
        self.assertIsInstance(self.nwb_file.electrodes[0][9], int)

        # ntrodes_extension - ntrode_id
        self.assertIsInstance(self.nwb_file.electrodes[0][10], int)

        # metadata_extension - rel_x
        self.assertIsInstance(self.nwb_file.electrodes[0][11], int)

        # metadata_extension - rel_y
        self.assertIsInstance(self.nwb_file.electrodes[0][12], int)

        # metadata_extension - rel_z
        self.assertIsInstance(self.nwb_file.electrodes[0][13], int)

    def test_injectExtensions_correctReturnValuesEqualsExtensions_true(self):
        header_extension = [0, 1, 2, 3]
        ntrodes_extension = [11, 11, 22, 22]

        self.electrode_extension_injector.inject_extensions(
            nwb_content=self.nwb_file,
            metadata_extension=self.mock_electrodes_metadata_extension,
            header_extension=header_extension,
            ntrodes_extension=ntrodes_extension
        )

        # header_extension - hw_chan
        self.assertEqual(self.nwb_file.electrodes[0][9], 0)
        self.assertEqual(self.nwb_file.electrodes[1][9], 1)
        self.assertEqual(self.nwb_file.electrodes[2][9], 2)
        self.assertEqual(self.nwb_file.electrodes[3][9], 3)

        # ntrodes_extension - ntrode_id
        self.assertEqual(self.nwb_file.electrodes[0][10], 11)
        self.assertEqual(self.nwb_file.electrodes[1][10], 11)
        self.assertEqual(self.nwb_file.electrodes[2][10], 22)
        self.assertEqual(self.nwb_file.electrodes[3][10], 22)

        # metadata_extension - rel_x
        self.assertEqual(self.nwb_file.electrodes[0][11], 0)
        self.assertEqual(self.nwb_file.electrodes[1][11], 0)
        self.assertEqual(self.nwb_file.electrodes[2][11], 0)
        self.assertEqual(self.nwb_file.electrodes[3][11], 0)

        # metadata_extension - rel_y
        self.assertEqual(self.nwb_file.electrodes[0][12], 1)
        self.assertEqual(self.nwb_file.electrodes[1][12], 1)
        self.assertEqual(self.nwb_file.electrodes[2][12], 1)
        self.assertEqual(self.nwb_file.electrodes[3][12], 1)

        # metadata_extension - rel_z
        self.assertEqual(self.nwb_file.electrodes[0][13], 2)
        self.assertEqual(self.nwb_file.electrodes[1][13], 2)
        self.assertEqual(self.nwb_file.electrodes[2][13], 2)
        self.assertEqual(self.nwb_file.electrodes[3][13], 2)

    def test_injectExtensions_raiseExceptionLongerHeaderExt_true(self):
        header_extension = [0, 1, 2, 3, 4, 5]
        ntrodes_extension = [11, 11, 22, 22]

        self.assertRaises(NotCompatibleMetadata,
                          self.electrode_extension_injector.inject_extensions,
                          self.nwb_file,
                          self.mock_electrodes_metadata_extension,
                          header_extension,
                          ntrodes_extension
                          )

    def test_injectExtensions_raiseExceptionLongerNtrodesExt_true(self):
        header_extension = [0, 1, 2, 3, 4]
        ntrodes_extension = [11, 11, 22, 22, 33]

        self.assertRaises(NotCompatibleMetadata,
                          self.electrode_extension_injector.inject_extensions,
                          self.nwb_file,
                          self.mock_electrodes_metadata_extension,
                          header_extension,
                          ntrodes_extension
                          )

    def test_injectExtensions_raiseExceptionShorterHeaderExt_true(self):
        header_extension = [0, 1, 2]
        ntrodes_extension = [11, 11, 22, 22]

        self.assertRaises(NotCompatibleMetadata,
                          self.electrode_extension_injector.inject_extensions,
                          self.nwb_file,
                          self.mock_electrodes_metadata_extension,
                          header_extension,
                          ntrodes_extension
                          )

    def test_injectExtensions_raiseExceptionShorterNtrodesExt_true(self):
        header_extension = [0, 1, 2, 3]
        ntrodes_extension = [11, 11, 22]

        self.assertRaises(NotCompatibleMetadata,
                          self.electrode_extension_injector.inject_extensions,
                          self.nwb_file,
                          self.mock_electrodes_metadata_extension,
                          header_extension,
                          ntrodes_extension
                          )

    def test_injectExtensions_properlyInjectEqualsExt_true(self):
        header_extension = [0, 1, 2, 3]
        ntrodes_extension = [11, 11, 22, 22]

        self.electrode_extension_injector.inject_extensions(
            nwb_content=self.nwb_file,
            metadata_extension=self.mock_electrodes_metadata_extension,
            header_extension=header_extension,
            ntrodes_extension=ntrodes_extension
        )

        self.assertIsNotNone(self.nwb_file.electrodes['rel_x'])
        self.assertIsNotNone(self.nwb_file.electrodes['rel_y'])
        self.assertIsNotNone(self.nwb_file.electrodes['rel_z'])
        self.assertIsNotNone(self.nwb_file.electrodes['hwChan'])
        self.assertIsNotNone(self.nwb_file.electrodes['ntrode_id'])
