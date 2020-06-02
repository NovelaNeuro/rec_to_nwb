from unittest import TestCase
from unittest.mock import MagicMock

import numpy as np
from pynwb import NWBFile
from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.nwb.components.mda.time.valid.fl_mda_valid_time_manager import FlMdaValidTimeManager


class TestMdaValidTimeManager(TestCase):

    def test_fl_mda_valid_time_manager_not_initialized_due_to_None_param(self):
        with self.assertRaises(TypeError):
            FlMdaValidTimeManager(None)

    def test_fl_mda_valid_time_manager_get_fl_mda_valid_times_with_gap_in_middle(self):
        sampling_rate = 1.0
        gaps_margin = 0.0001
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 7, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.acquisition['e-series'].timestamps = mock_array
        mock_metadata = {}

        fl_mda_valid_time_manager = FlMdaValidTimeManager(sampling_rate, mock_metadata)
        fl_mda_valid_times = fl_mda_valid_time_manager.get_fl_mda_valid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )

        self.assertEqual(len(fl_mda_valid_times), 2)
        self.assertEqual(round(fl_mda_valid_times[0].start_time, 4), 1.0001)
        self.assertEqual(round(fl_mda_valid_times[0].stop_time, 4), 4.9999)
        self.assertEqual(round(fl_mda_valid_times[1].start_time, 4), 9.0001)
        self.assertEqual(round(fl_mda_valid_times[1].stop_time, 4), 11.9999)

    def test_fl_mda_valid_time_manager_get_fl_mda_valid_times_without_gap(self):
        sampling_rate = 1.0
        gaps_margin = 0.0001
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.acquisition['e-series'].timestamps = mock_array
        mock_metadata = {'times_period_multiplier': 1.5}

        fl_mda_valid_time_manager = FlMdaValidTimeManager(sampling_rate, mock_metadata)
        fl_mda_valid_times = fl_mda_valid_time_manager.get_fl_mda_valid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )

        self.assertEqual(len(fl_mda_valid_times), 1)
        self.assertEqual(round(fl_mda_valid_times[0].start_time, 4), 1.0001)
        self.assertEqual(round(fl_mda_valid_times[0].stop_time, 4), 9.9999)

    def test_fl_mda_valid_time_manager_get_fl_mda_valid_times_with_gap_at_start(self):
        sampling_rate = 1.0
        gaps_margin = 0.0001
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 3, 5, 6, 7, 8, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.acquisition['e-series'].timestamps = mock_array
        mock_metadata = {'times_period_multiplier': 1.5}

        fl_mda_valid_time_manager = FlMdaValidTimeManager(sampling_rate, mock_metadata)
        fl_mda_valid_times = fl_mda_valid_time_manager.get_fl_mda_valid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )

        self.assertEqual(len(fl_mda_valid_times), 1)
        self.assertEqual(round(fl_mda_valid_times[0].start_time, 4), 5.0001)
        self.assertEqual(round(fl_mda_valid_times[0].stop_time, 4), 11.9999)

    def test_fl_mda_valid_time_manager_get_fl_mda_valid_times_with_gap_at_end(self):
        sampling_rate = 1.0
        gaps_margin = 0.0001
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.acquisition['e-series'].timestamps = mock_array
        mock_metadata = {'times_period_multiplier': 1.5}

        fl_mda_valid_time_manager = FlMdaValidTimeManager(sampling_rate, mock_metadata)
        fl_mda_valid_times = fl_mda_valid_time_manager.get_fl_mda_valid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )

        self.assertEqual(len(fl_mda_valid_times), 1)
        self.assertEqual(round(fl_mda_valid_times[0].start_time, 4), 1.0001)
        self.assertEqual(round(fl_mda_valid_times[0].stop_time, 4), 7.9999)

    @should_raise(TypeError)
    def test_fl_mda_valid_time_manager_get_fl_mda_valid_times_failed_due_to_None_param(self):
        gaps_margin = 0.0001
        sampling_rate = 1.0
        mock_metadata = {'times_period_multiplier': 1.5}

        fl_mda_valid_time_manager = FlMdaValidTimeManager(sampling_rate, mock_metadata)
        fl_mda_valid_time_manager.get_fl_mda_valid_times(
            nwb_content=None,
            gaps_margin=gaps_margin
        )

    @should_raise(MissingDataException)
    def test_fl_mda_valid_time_manager_get_fl_mda_valid_times_failed_due_to_lack_of_timestamps(self):
        gaps_margin = 0.0001
        sampling_rate = 1.0
        mock_nwb = MagicMock(spec=NWBFile)
        mock_nwb.acquisition['e-series'].timestamps = None
        mock_metadata = {'times_period_multiplier': 1.5}

        fl_mda_valid_time_manager = FlMdaValidTimeManager(sampling_rate, mock_metadata)
        fl_mda_valid_time_manager.get_fl_mda_valid_times(
            nwb_content=mock_nwb,
            gaps_margin=gaps_margin
        )