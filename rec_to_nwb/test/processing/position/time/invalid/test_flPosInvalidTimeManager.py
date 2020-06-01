from unittest import TestCase
from unittest.mock import MagicMock

import numpy as np
from pynwb import NWBFile
from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.nwb.components.position.time.invalid.fl_pos_invalid_time_manager import \
    FlPosInvalidTimeManager


class TestFlPosInvalidTimeManager(TestCase):

    def test_fl_pos_invalid_time_manager_get_fl_pos_invalid_times_with_gap_in_middle(self):
        gaps_margin = 0.0001
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 2, 3, 4, 5, 7, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.processing['behavior'].data_interfaces['position'].spatial_series['series'].timestamps = mock_array

        fl_pos_invalid_time_manager = FlPosInvalidTimeManager()
        fl_pos_invalid_times = fl_pos_invalid_time_manager.get_fl_pos_invalid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )

        self.assertEqual(len(fl_pos_invalid_times), 1)
        self.assertEqual(round(fl_pos_invalid_times[0].start_time, 4), 5 + gaps_margin)
        self.assertEqual(round(fl_pos_invalid_times[0].stop_time, 4),  9 - gaps_margin)

    def test_fl_pos_invalid_time_manager_get_fl_pos_invalid_times_without_gap(self):
        gaps_margin = 0.0001
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.processing['behavior'].data_interfaces['position'].spatial_series['series'].timestamps = mock_array

        fl_pos_invalid_time_manager = FlPosInvalidTimeManager()
        fl_pos_invalid_times = fl_pos_invalid_time_manager.get_fl_pos_invalid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )

        self.assertEqual(fl_pos_invalid_times, [])

    def test_fl_pos_invalid_time_manager_get_fl_pos_invalid_times_with_gap_at_start(self):
        gaps_margin = 0.0001
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 3, 5, 6, 7, 8, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.processing['behavior'].data_interfaces['position'].spatial_series['series'].timestamps = mock_array

        fl_pos_invalid_time_manager = FlPosInvalidTimeManager()
        fl_pos_invalid_times = fl_pos_invalid_time_manager.get_fl_pos_invalid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )

        self.assertEqual(len(fl_pos_invalid_times), 1)
        self.assertEqual(round(fl_pos_invalid_times[0].start_time, 4),  1 + gaps_margin)
        self.assertEqual(round(fl_pos_invalid_times[0].stop_time, 4), 5 - gaps_margin)

    def test_fl_pos_invalid_time_manager_get_fl_pos_invalid_times_with_gap_at_end(self):
        gaps_margin = 0.0001
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.processing['behavior'].data_interfaces['position'].spatial_series['series'].timestamps = mock_array

        fl_pos_invalid_time_manager = FlPosInvalidTimeManager()
        fl_pos_invalid_times = fl_pos_invalid_time_manager.get_fl_pos_invalid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )

        self.assertEqual(len(fl_pos_invalid_times), 1)
        self.assertEqual(round(fl_pos_invalid_times[0].start_time, 4), 8 + gaps_margin)
        self.assertEqual(round(fl_pos_invalid_times[0].stop_time, 4), 12 - gaps_margin)

    def test_fl_pos_invalid_time_manager_get_fl_pos_invalid_times_with_two_gaps(self):
        gaps_margin = 0.0001
        mock_array = np.ndarray(dtype='float', shape=[12, ])
        array = [1, 2, 6, 12, 13, 14, 20, 25, 26, 27, 28, 29]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.processing['behavior'].data_interfaces['position'].spatial_series['series'].timestamps = mock_array

        fl_pos_invalid_time_manager = FlPosInvalidTimeManager()
        fl_pos_invalid_times = fl_pos_invalid_time_manager.get_fl_pos_invalid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )

        self.assertEqual(len(fl_pos_invalid_times), 2)
        self.assertEqual(round(fl_pos_invalid_times[0].start_time, 4), 2 + gaps_margin)
        self.assertEqual(round(fl_pos_invalid_times[0].stop_time, 4), 12 - gaps_margin)
        self.assertEqual(round(fl_pos_invalid_times[1].start_time, 4), 14 + gaps_margin)
        self.assertEqual(round(fl_pos_invalid_times[1].stop_time, 4), 25 - gaps_margin)

    @should_raise(TypeError)
    def test_fl_pos_invalid_time_manager_get_fl_pos_invalid_times_failed_due_to_None_param(self):
        gaps_margin = 0.0001

        fl_pos_invalid_time_manager = FlPosInvalidTimeManager()
        fl_pos_invalid_time_manager.get_fl_pos_invalid_times(
            nwb_content=None,
            gaps_margin=gaps_margin
        )

    @should_raise(MissingDataException)
    def test_fl_pos_invalid_time_manager_get_fl_pos_invalid_times_failed_due_to_lack_of_timestamps(self):
        gaps_margin = 0.0001
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.processing['behavior'].data_interfaces['position'].spatial_series['series'].timestamps = None

        fl_pos_invalid_time_manager = FlPosInvalidTimeManager()
        fl_pos_invalid_time_manager.get_fl_pos_invalid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )



