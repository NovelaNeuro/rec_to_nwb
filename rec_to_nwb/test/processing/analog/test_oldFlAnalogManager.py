from unittest import TestCase
from unittest.mock import patch

import numpy as np
from numpy.testing import assert_array_equal
from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.not_equal_param_length_exception import NotEqualParamLengthException
from rec_to_nwb.processing.nwb.components.analog.old_fl_analog_extractor import OldFlAnalogExtractor
from rec_to_nwb.processing.nwb.components.analog.old_fl_analog_manager import OldFlAnalogManager


class TestOldFlAnalogManager(TestCase):

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
            'timestamps': []
        }

    @patch.object(OldFlAnalogExtractor, 'extract_analog_for_single_dataset', new=fake_extract_analog_for_single_dataset)
    def test_get_analog_returnCorrectData_successfully(self):
        mock_analog_files = [{1: 'mocked'}, {2: 'mocked'}]

        old_analog_manager = OldFlAnalogManager(
            analog_files=mock_analog_files
        )
        old_fl_analog = old_analog_manager.get_analog()
        transposed_analog_data, timestamps = old_fl_analog.data, old_fl_analog.timestamps

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
            np.array([])
        )

    @should_raise(TypeError)
    def test_get_analog_fails_due_to_None_param(self):
        OldFlAnalogManager(
            analog_files=None
        )

