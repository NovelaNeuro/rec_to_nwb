from unittest import TestCase
from unittest.mock import Mock
import numpy as np

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_manager import FlInvalidTimeManager
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_pos_timestamp_extractor import \
    FlInvalidTimePosTimestampExtractor
from fl.datamigration.nwb.components.invalid_times.fl_pos_invalid_time_manager import FlPosInvalidTimeManager


class TestPosInvalidTimesManager(TestCase):
    def test_input_validation(self):
        with self.assertRaises(NoneParamException):
            FlInvalidTimeManager(None)

    def test_gap_in_the_middle(self):
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 7, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        extractor_mock = Mock(spec=FlInvalidTimePosTimestampExtractor)
        extractor_mock.get_converted_timestamps = Mock(return_value=[mock_array])
        manager = FlPosInvalidTimeManager([])
        manager.pos_timestamps_extractor = extractor_mock
        invalid_times = manager.build_pos_invalid_times()
        self.assertEqual(1, len(invalid_times))
        self.assertEqual(5, invalid_times[0].start_time)
        self.assertEqual(9, invalid_times[0].stop_time)

    def test_no_gap(self):
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i, number in enumerate(array):
            mock_array[i] = number
        extractor_mock = Mock(spec=FlInvalidTimePosTimestampExtractor)
        extractor_mock.get_converted_timestamps = Mock(return_value=[mock_array])
        manager = FlPosInvalidTimeManager([])
        manager.pos_timestamps_extractor = extractor_mock
        invalid_times = manager.build_pos_invalid_times()
        self.assertEqual([], invalid_times)

    def test_gap_at_start(self):
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 3, 5, 6, 7, 8, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        extractor_mock = Mock(spec=FlInvalidTimePosTimestampExtractor)
        extractor_mock.get_converted_timestamps = Mock(return_value=[mock_array])
        manager = FlPosInvalidTimeManager([])
        manager.pos_timestamps_extractor = extractor_mock
        invalid_times = manager.build_pos_invalid_times()
        self.assertEqual(1, len(invalid_times))
        self.assertEqual(1, invalid_times[0].start_time)
        self.assertEqual(5, invalid_times[0].stop_time)

    def test_gap_at_the_end(self):
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        extractor_mock = Mock(spec=FlInvalidTimePosTimestampExtractor)
        extractor_mock.get_converted_timestamps = Mock(return_value=[mock_array])
        manager = FlPosInvalidTimeManager([])
        manager.pos_timestamps_extractor = extractor_mock
        invalid_times = manager.build_pos_invalid_times()
        self.assertEqual(1, len(invalid_times))
        self.assertEqual(8, invalid_times[0].start_time)
        self.assertEqual(12, invalid_times[0].stop_time)