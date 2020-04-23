from unittest import TestCase
from unittest.mock import Mock

from fl.datamigration.nwb.components.invalid_times.fl_mda_invalid_time_manager import FlMdaInvalidTimeManager
from fl.datamigration.nwb.components.invalid_times.fl_mda_invalid_times import FlMdaInvalidTime


class TestFlMdaInvalidTimesManager(TestCase):

    def test_fl_pos_invalid_time_manager_create_fl_invalid_times_successfully(self):

        mock_datasets = Mock(spec=list)

        fl_mda_invalid_time_manager = FlMdaInvalidTimeManager(
            datasets=mock_datasets
        )
        fl_mda_invalid_times = fl_mda_invalid_time_manager.get_fl_mda_invalid_times()

        self.assertIsInstance(fl_mda_invalid_times, list)
        self.assertIsInstance(fl_mda_invalid_times[0], FlMdaInvalidTime)

        self.assertEqual(fl_mda_invalid_times, None)
        self.assertEqual(fl_mda_invalid_times[0].start_time, None)
        self.assertEqual(fl_mda_invalid_times[0].stop_time, None)


