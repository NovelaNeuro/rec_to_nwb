import os
from unittest import TestCase
from unittest.mock import Mock

from pynwb import NWBFile

from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.nwb_builder.builders.electrode_builder import ElectrodeBuilder
from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata

path = os.path.dirname(os.path.abspath(__file__))


class TestElectrodeBuilder(TestCase):

    def setUp(self):
        self.metadata = NWBMetadata(str(path) + '/res/nwb_elements_builder_test/metadata.yml',
                                    [str(path) + '/res/nwb_elements_builder_test/probe1.yml',
                                     str(path) + '/res/nwb_elements_builder_test/probe2.yml',
                                     str(path) + '/res/nwb_elements_builder_test/probe3.yml'])

        self.electrodes_builder = ElectrodeBuilder(self.metadata.probes, self.metadata.metadata['electrode groups'])

    def test_build_successful_creation(self):
        # given
        mock_nwb = Mock()
        mock_nwb.__class__ = NWBFile

        mock_eg_1 = Mock()
        mock_eg_2 = Mock()
        mock_eg_1.__class__ = FLElectrodeGroup
        mock_eg_2.__class__ = FLElectrodeGroup
        electrode_group_object_dict = {0: mock_eg_1, 1: mock_eg_2}

        # when
        self.electrodes_builder.build(
            nwb_content=mock_nwb,
            electrode_group_dict=electrode_group_object_dict,
        )
        # ToDo Need idea how to test it with mock_nwb

        # then
        # self.assertEqual(256, len(electrodes))
        # self.assertIsInstance(electrodes[0], DynamicTable)
        # self.assertIsInstance(electrodes[1], DynamicTable)
