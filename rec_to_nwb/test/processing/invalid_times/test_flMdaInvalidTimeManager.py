from unittest import TestCase
from unittest.mock import Mock

from rec_to_nwb.processing.nwb.components.mda_invalid_times.fl_invalid_time_mda_timestamp_extractor import \
    FlInvalidTimeMdaTimestampExtractor
from rec_to_nwb.processing.nwb.components.mda_invalid_times.fl_mda_invalid_time_manager import FlMdaInvalidTimeManager

import numpy as np


class TestMdaInvalidTimesManager(TestCase):
    def test_mda_invalid_times_manager_input_validation(self):
        with self.assertRaises(TypeError):
            FlMdaInvalidTimeManager(None, [])
            FlMdaInvalidTimeManager(1, None)

    def test_mda_invalid_times_manager_data_with_gap_in_the_middle(self):
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 7, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_continuous_time_dict = {str(float(i)) : float(i) * 1E9 for i in range(20)}
        extractor_mock = Mock(spec=FlInvalidTimeMdaTimestampExtractor)
        extractor_mock.get_continuous_time_dict = Mock(return_value=mock_continuous_time_dict)
        extractor_mock.get_sample_count_from_single_epoch = Mock(return_value=mock_array)
        manager = FlMdaInvalidTimeManager(1000000000.0, ['test'])
        manager.fl_invalid_time_mda_extractor = extractor_mock

        invalid_times = manager.get_mda_invalid_times()

        self.assertEqual(len(invalid_times), 1)
        self.assertEqual(invalid_times[0].start_time, 5)
        self.assertEqual(invalid_times[0].stop_time, 9)

    def test_mda_invalid_times_manager_data_with_no_gap(self):
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_continuous_time_dict = {str(float(i)) : float(i) * 1E9 for i in range(20)}
        extractor_mock = Mock(spec=FlInvalidTimeMdaTimestampExtractor)
        extractor_mock.get_continuous_time_dict = Mock(return_value=mock_continuous_time_dict)
        extractor_mock.get_sample_count_from_single_epoch = Mock(return_value=mock_array)
        manager = FlMdaInvalidTimeManager(1000000000.0, ['test'])
        manager.fl_invalid_time_mda_extractor = extractor_mock

        invalid_times = manager.get_mda_invalid_times()

        self.assertEqual(invalid_times, [])

    def test_mda_invalid_times_manager_data_with_gap_at_start(self):
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 3, 5, 6, 7, 8, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_continuous_time_dict = {str(float(i)) : float(i) * 1E9 for i in range(20)}
        extractor_mock = Mock(spec=FlInvalidTimeMdaTimestampExtractor)
        extractor_mock.get_continuous_time_dict = Mock(return_value=mock_continuous_time_dict)
        extractor_mock.get_sample_count_from_single_epoch = Mock(return_value=mock_array)
        manager = FlMdaInvalidTimeManager(1000000000.0, ['test'])
        manager.fl_invalid_time_mda_extractor = extractor_mock

        invalid_times = manager.get_mda_invalid_times()

        self.assertEqual(len(invalid_times), 1)
        self.assertEqual(invalid_times[0].start_time, 1)
        self.assertEqual(invalid_times[0].stop_time, 5)

    def test_mda_invalid_times_manager_data_with_gap_at_end(self):
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_continuous_time_dict = {str(float(i)) : float(i) * 1E9 for i in range(20)}
        extractor_mock = Mock(spec=FlInvalidTimeMdaTimestampExtractor)
        extractor_mock.get_continuous_time_dict = Mock(return_value=mock_continuous_time_dict)
        extractor_mock.get_sample_count_from_single_epoch = Mock(return_value=mock_array)
        manager = FlMdaInvalidTimeManager(1000000000.0, ['test'])
        manager.fl_invalid_time_mda_extractor = extractor_mock

        invalid_times = manager.get_mda_invalid_times()

        self.assertEqual(len(invalid_times), 1)
        self.assertEqual(invalid_times[0].start_time, 8)
        self.assertEqual(invalid_times[0].stop_time, 12)
