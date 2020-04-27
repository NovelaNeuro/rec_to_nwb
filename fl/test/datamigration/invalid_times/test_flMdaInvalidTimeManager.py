from unittest import TestCase
from unittest.mock import Mock
import numpy as np

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_manager import FlInvalidTimeManager
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_mda_timestamp_extractor import \
    FlInvalidTimeMdaTimestampExtractor
from fl.datamigration.nwb.components.invalid_times.fl_mda_invalid_time_manager import FlMdaInvalidTimeManager


class TestMdaInvalidTimesManager(TestCase):
    def test_input_validation(self):
        with self.assertRaises(NoneParamException):
            FlInvalidTimeManager(None)

    def test_build_invalid_times(self):
        mock_array = np.ndarray(dtype='float', shape=[10,])
        array = [1, 2, 3, 4, 5, 7, 9, 10, 11, 12]
        for i, number in enumerate(array):
            mock_array[i] = number
        extractor_mock = Mock(spec=FlInvalidTimeMdaTimestampExtractor)
        extractor_mock.get_converted_timestamps = Mock(return_value=[mock_array])
        manager = FlMdaInvalidTimeManager(1000000000, [])
        manager.timestamps_extractor = extractor_mock
        invalid_times = manager.build_mda_invalid_times()
        self.assertEqual(1, len(invalid_times))
        self.assertEqual(5, invalid_times[0].start_time)
        self.assertEqual(9, invalid_times[0].stop_time)


