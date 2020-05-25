from unittest import TestCase
from unittest.mock import Mock

import numpy as np
from rec_to_nwb.processing.nwb.components.mda_invalid_times.fl_mda_invalid_time_fl_mda_invalid_time_manager import \
    FlMdaInvalidTimeManager


class TestMdaInvalidTimesManager(TestCase):

    def test_mda_invalid_times_fl_mda_invalid_time_manager_input_validation(self):
        with self.assertRaises(TypeError):
            FlMdaInvalidTimeManager(None)

    def test_mda_invalid_times_fl_mda_invalid_time_manager_data_with_gap_in_the_middle(self):
        sampling_rate = 1000000000.0
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 7, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number

        fl_mda_invalid_time_manager = FlMdaInvalidTimeManager(sampling_rate)
        fl_mda_invalid_time_manager.fl_invalid_time_mda_extractor = extractor_mock

        invalid_times = fl_mda_invalid_time_manager.get_mda_invalid_times()

        self.assertEqual(len(invalid_times), 1)
        self.assertEqual(round(invalid_times[0].start_time, 4), 5.0001)
        self.assertEqual(round(invalid_times[0].stop_time, 4), 8.9999)

    def test_mda_invalid_times_fl_mda_invalid_time_manager_data_with_no_gap(self):
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_continuous_time_dict = {str(float(i)) : float(i) * 1E9 for i in range(20)}
        extractor_mock = Mock(spec=FlInvalidTimeMdaTimestampExtractor)
        extractor_mock.get_continuous_time_dict = Mock(return_value=mock_continuous_time_dict)
        extractor_mock.get_sample_count_from_single_epoch = Mock(return_value=mock_array)
        fl_mda_invalid_time_manager = FlMdaInvalidTimeManager(1000000000.0, ['test'])
        fl_mda_invalid_time_manager.fl_invalid_time_mda_extractor = extractor_mock

        invalid_times = fl_mda_invalid_time_manager.get_mda_invalid_times()

        self.assertEqual(invalid_times, [])

    def test_mda_invalid_times_fl_mda_invalid_time_manager_data_with_gap_at_start(self):
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 3, 5, 6, 7, 8, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_continuous_time_dict = {str(float(i)) : float(i) * 1E9 for i in range(20)}
        extractor_mock = Mock(spec=FlInvalidTimeMdaTimestampExtractor)
        extractor_mock.get_continuous_time_dict = Mock(return_value=mock_continuous_time_dict)
        extractor_mock.get_sample_count_from_single_epoch = Mock(return_value=mock_array)
        fl_mda_invalid_time_manager = FlMdaInvalidTimeManager(1000000000.0, ['test'])
        fl_mda_invalid_time_manager.fl_invalid_time_mda_extractor = extractor_mock

        invalid_times = fl_mda_invalid_time_manager.get_mda_invalid_times()

        self.assertEqual(len(invalid_times), 1)
        self.assertEqual(round(invalid_times[0].start_time, 4), 1.0001)
        self.assertEqual(round(invalid_times[0].stop_time, 4), 4.9999)

    def test_mda_invalid_times_fl_mda_invalid_time_manager_data_with_gap_at_end(self):
        mock_array = np.ndarray(dtype='float', shape=[10, ])
        array = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        mock_continuous_time_dict = {str(float(i)) : float(i) * 1E9 for i in range(20)}
        extractor_mock = Mock(spec=FlInvalidTimeMdaTimestampExtractor)
        extractor_mock.get_continuous_time_dict = Mock(return_value=mock_continuous_time_dict)
        extractor_mock.get_sample_count_from_single_epoch = Mock(return_value=mock_array)
        fl_mda_invalid_time_manager = FlMdaInvalidTimeManager(1000000000.0, ['test'])
        fl_mda_invalid_time_manager.fl_invalid_time_mda_extractor = extractor_mock

        invalid_times = fl_mda_invalid_time_manager.get_mda_invalid_times()

        self.assertEqual(len(invalid_times), 1)
        self.assertEqual(round(invalid_times[0].start_time, 4), 8.0001)
        self.assertEqual(round(invalid_times[0].stop_time, 4), 11.9999)
