from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dateutil.tz import tzlocal
from pynwb import NWBFile
from pynwb.ecephys import ElectrodeGroup

from src.datamigration.nwb.components.electrode_group.electrode_group_injector import ElectrodeGroupInjector


class TestElectrodeGroupInjector(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        cls.mock_electrode_group_1 = Mock(spec=ElectrodeGroup)
        cls.mock_electrode_group_2 = Mock(spec=ElectrodeGroup)
        cls.mock_electrode_group_3 = Mock(spec=ElectrodeGroup)
        cls.electrode_group_dict = {'1': cls.mock_electrode_group_1, '2': cls.mock_electrode_group_2,
                                    '3': cls.mock_electrode_group_3}

        electrode_group = ElectrodeGroupInjector()
        electrode_group.inject_all_electrode_groups(cls.nwb_file, cls.electrode_group_dict)

    def test_injectAllElectrodeGroups_returnCorrectValues_true(self):
        self.assertEqual(self.nwb_file.electrode_groups, {
            self.mock_electrode_group_1.name: self.mock_electrode_group_1,
            self.mock_electrode_group_2.name: self.mock_electrode_group_2,
            self.mock_electrode_group_3.name: self.mock_electrode_group_3}
                         )

    def test_injectAllElectrodeGroups_returnCorrectType_true(self):
        self.assertIsInstance(self.nwb_file.electrode_groups, dict)
