from unittest import TestCase
from unittest.mock import Mock

from rec_to_nwb.processing.nwb.components.pos_invalid_times.fl_invalid_time_pos_timestamp_extractor import \
    FlInvalidTimePosTimestampExtractor
from rec_to_nwb.processing.nwb.components.pos_invalid_times.fl_pos_invalid_time_manager import FlPosInvalidTimeManager

import numpy as np


class TestPosInvalidTimesManager(TestCase):
    def test_pos_invalid_times_manager_input_validation(self):
        with self.assertRaises(TypeError):
            FlPosInvalidTimeManager(None)

    def test_pos_invalid_times_manager_data_with_gap_in_the_middle(self):
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 7, 9, 10, 11, 12]
        eps = 0.0001
        for i, number in enumerate(array):
            mock_array[i] = number
        extractor_mock = Mock(spec=FlInvalidTimePosTimestampExtractor)
        extractor_mock.get_converted_timestamps = Mock(return_value=[mock_array])
        manager = FlPosInvalidTimeManager([])
        manager.pos_timestamps_extractor = extractor_mock

        invalid_times = manager.get_pos_invalid_times()

        self.assertEqual(len(invalid_times), 1)
        self.assertEqual(round(invalid_times[0].start_time, 4), 5 + eps)
        self.assertEqual(round(invalid_times[0].stop_time, 4),  9 - eps)

    def test_pos_invalid_times_manager_data_with_no_gap(self):
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i, number in enumerate(array):
            mock_array[i] = number
        extractor_mock = Mock(spec=FlInvalidTimePosTimestampExtractor)
        extractor_mock.get_converted_timestamps = Mock(return_value=[mock_array])
        manager = FlPosInvalidTimeManager([])
        manager.pos_timestamps_extractor = extractor_mock

        invalid_times = manager.get_pos_invalid_times()

        self.assertEqual(invalid_times, [])

    def test_pos_invalid_times_manager_data_with_gap_at_start(self):
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 3, 5, 6, 7, 8, 9, 10, 11, 12]
        eps = 0.0001
        for i, number in enumerate(array):
            mock_array[i] = number
        extractor_mock = Mock(spec=FlInvalidTimePosTimestampExtractor)
        extractor_mock.get_converted_timestamps = Mock(return_value=[mock_array])
        manager = FlPosInvalidTimeManager([])
        manager.pos_timestamps_extractor = extractor_mock

        invalid_times = manager.get_pos_invalid_times()

        self.assertEqual(len(invalid_times), 1)
        self.assertEqual(round(invalid_times[0].start_time, 4),  1 + eps)
        self.assertEqual(round(invalid_times[0].stop_time, 4), 5 - eps)

    def test_pos_invalid_times_manager_data_with_gap_at_the_end(self):
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        eps = 0.0001
        array = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        extractor_mock = Mock(spec=FlInvalidTimePosTimestampExtractor)
        extractor_mock.get_converted_timestamps = Mock(return_value=[mock_array])
        manager = FlPosInvalidTimeManager([])
        manager.pos_timestamps_extractor = extractor_mock

        invalid_times = manager.get_pos_invalid_times()

        self.assertEqual(len(invalid_times), 1)
        self.assertEqual(round(invalid_times[0].start_time, 4), 8 + eps)
        self.assertEqual(round(invalid_times[0].stop_time, 4), 12 - eps)