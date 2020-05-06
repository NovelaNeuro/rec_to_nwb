from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dateutil.tz import tzlocal
from pynwb import NWBFile
from pynwb.ecephys import ElectrodeGroup
from testfixtures import should_raise

from fldatamigration.processing.exceptions.none_param_exception import NoneParamException
from fldatamigration.processing.nwb.components.electrode_group.electrode_group_injector import ElectrodeGroupInjector


class TestElectrodeGroupInjector(TestCase):

    def setUp(self):
        self.nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        self.electrode_group = ElectrodeGroupInjector()

    def test_injector_inject_ElectrodeGroups_to_nwb_successfully(self):
        mock_electrode_group_1 = Mock(spec=ElectrodeGroup)
        mock_electrode_group_2 = Mock(spec=ElectrodeGroup)
        mock_electrode_group_3 = Mock(spec=ElectrodeGroup)
        electrode_group_dict = {mock_electrode_group_1.name: mock_electrode_group_1,
                                mock_electrode_group_2.name: mock_electrode_group_2,
                                mock_electrode_group_3.name: mock_electrode_group_3}

        self.electrode_group.inject_all_electrode_groups(
            nwb_content=self.nwb_file,
            electrode_groups=[
                mock_electrode_group_1,
                mock_electrode_group_2,
                mock_electrode_group_3
            ]
        )

        self.assertIsInstance(self.nwb_file.electrode_groups, dict)
        self.assertEqual(self.nwb_file.electrode_groups, electrode_group_dict)

    @should_raise(NoneParamException)
    def test_injector_failed_inject_ElectrodeGroups_to_nwb_due_to_None_ElectrodeGroups(self):
        self.electrode_group.inject_all_electrode_groups(
            nwb_content=self.nwb_file,
            electrode_groups=None
        )
