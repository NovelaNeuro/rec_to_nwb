from unittest import TestCase

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_manager import InvalidTimeManager

class TestInvalidTimesManager(TestCase):
    def test_input_validation(self):
        with self.assertRaises(NoneParamException):
            InvalidTimeManager(None, [])
        with self.assertRaises(NoneParamException):
            InvalidTimeManager(1, None)
