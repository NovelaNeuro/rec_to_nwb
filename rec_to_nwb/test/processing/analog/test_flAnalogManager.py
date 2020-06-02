from unittest import TestCase
from unittest.mock import patch
import numpy as np
from numpy.testing import assert_array_equal
from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.not_equal_param_length_exception import NotEqualParamLengthException
from rec_to_nwb.processing.nwb.components.analog.fl_analog_extractor import FlAnalogExtractor
from rec_to_nwb.processing.nwb.components.analog.fl_analog_manager import FlAnalogManager


class TestFlAnalogManager(TestCase):

    @staticmethod
    def fake_extract_analog_for_single_dataset(*args, **kwargs):
        return {
            'AccelX': [1, 11, 111],
            'AccelY': [2, 22, 222],
            'AccelZ': [3, 33, 333],
            'GyroX': [4, 44, 444],
            'GyroY': [5, 55, 555],
            'GyroZ': [6, 66, 666],
            'MagX': [7, 77, 777],
            'MagY': [8, 88, 888],
            'MagZ': [9, 99, 999],
            'timestamps': [123, 234, 456]
        }

    @patch.object(FlAnalogExtractor, 'extract_analog_for_single_dataset', new=fake_extract_analog_for_single_dataset)
    def test_get_analog_returnCorrectData_successfully(self):
        mock_analog_files = [{1: 'mocked'}, {2: 'mocked'}]
        mock_continuous_time_files = ['Mock1', 'Mock2']

        analog_manager = FlAnalogManager(
            analog_files=mock_analog_files,
            continuous_time_files=mock_continuous_time_files
        )
        fl_analog = analog_manager.get_analog()
        transposed_analog_data, timestamps =  fl_analog.data, fl_analog.timestamps

        assert_array_equal(
            transposed_analog_data,
            np.array([
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [11, 22, 33, 44, 55, 66, 77, 88, 99],
                [111, 222, 333, 444, 555, 666, 777, 888, 999],
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [11, 22, 33, 44, 55, 66, 77, 88, 99],
                [111, 222, 333, 444, 555, 666, 777, 888, 999]
            ])
        )
        self.assertIsInstance(transposed_analog_data, np.ndarray)

        assert_array_equal(
            timestamps,
            np.array([123, 234, 456, 123, 234, 456])
        )
        self.assertIsInstance(timestamps, np.ndarray)

    @should_raise(TypeError)
    def test_get_analog_fails_due_to_None_param(self):
        mock_continuous_time_files = ['Mock1', 'Mock2']
        FlAnalogManager(
            analog_files=None,
            continuous_time_files=mock_continuous_time_files
        )

    @should_raise(NotEqualParamLengthException)
    def test_get_analog_fails_due_to_different_param_length(self):
        mock_analog_files = [{1: 'mocked'}]
        mock_continuous_time_files = ['Mock1', 'Mock2']

        FlAnalogManager(
            analog_files=mock_analog_files,
            continuous_time_files=mock_continuous_time_files
        )
