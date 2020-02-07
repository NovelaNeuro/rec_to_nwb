import unittest
from datetime import datetime
from unittest.mock import Mock

from dateutil.tz import tzlocal
from hdmf.common import VectorData
from pynwb import NWBFile

from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.nwb_builder.builders.electrode_builder import ElectrodeBuilder
from src.datamigration.nwb_builder.creators.electrode_metadata_extension_creator import \
    ElectrodesMetadataExtensionCreator
from src.datamigration.nwb_builder.injectors.electrode_extension_injector import ElectrodeExtensionInjector


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

    def test_injectExtensions_correctTypeInsideNWB_true(self):
        hw_chan = [0, 1, 2, 3]

        self.electrode_extension_injector.inject_extensions(
            nwb_content=self.nwb_file,
            electrodes_metadata_extension=self.mock_electrodes_metadata_extension,
            hw_chan=hw_chan
        )

        self.assertIsInstance(self.nwb_file.electrodes[0][9], int)
        self.assertIsInstance(self.nwb_file.electrodes[0][10], int)
        self.assertIsInstance(self.nwb_file.electrodes[0][11], int)
        self.assertIsInstance(self.nwb_file.electrodes[0][12], int)

    def test_injectExtensions_correctValuesInsideNWB_true(self):
        hw_chan = [0, 1, 2, 3]

        self.electrode_extension_injector.inject_extensions(
            nwb_content=self.nwb_file,
            electrodes_metadata_extension=self.mock_electrodes_metadata_extension,
            hw_chan=hw_chan
        )

        self.assertIsInstance(self.nwb_file.electrodes['rel_x'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['rel_y'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['rel_z'], VectorData)
        self.assertIsInstance(self.nwb_file.electrodes['hwChan'], VectorData)

    def test_injectExtensions_properlyInjectEqualHwChan_true(self):
        hw_chan = [0, 1, 2, 3]

        self.electrode_extension_injector.inject_extensions(
            nwb_content=self.nwb_file,
            electrodes_metadata_extension=self.mock_electrodes_metadata_extension,
            hw_chan=hw_chan
        )

        self.assertIsNotNone(self.nwb_file.electrodes['rel_x'])
        self.assertIsNotNone(self.nwb_file.electrodes['rel_y'])
        self.assertIsNotNone(self.nwb_file.electrodes['rel_z'])
        self.assertIsNotNone(self.nwb_file.electrodes['hwChan'])

    def test_injectExtensions_properlyInjectShorterHwChan_true(self):
        hw_chan = [0, 1, 2]

        self.electrode_extension_injector.inject_extensions(
            nwb_content=self.nwb_file,
            electrodes_metadata_extension=self.mock_electrodes_metadata_extension,
            hw_chan=hw_chan
        )
        self.assertIsNotNone(self.nwb_file.electrodes['rel_x'])
        self.assertIsNotNone(self.nwb_file.electrodes['rel_y'])
        self.assertIsNotNone(self.nwb_file.electrodes['rel_z'])
        self.assertIsNotNone(self.nwb_file.electrodes['hwChan'])

    def test_injectExtensions_properlyInjectLongerHwChan_true(self):
        hw_chan = [0, 1, 2, 3, 4, 5]

        self.electrode_extension_injector.inject_extensions(
            nwb_content=self.nwb_file,
            electrodes_metadata_extension=self.mock_electrodes_metadata_extension,
            hw_chan=hw_chan
        )

        self.assertIsNotNone(self.nwb_file.electrodes['rel_x'])
        self.assertIsNotNone(self.nwb_file.electrodes['rel_y'])
        self.assertIsNotNone(self.nwb_file.electrodes['rel_z'])
        self.assertIsNotNone(self.nwb_file.electrodes['hwChan'])
