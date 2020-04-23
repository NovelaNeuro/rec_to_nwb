from unittest import TestCase

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_manager import FlInvalidTimeManager

class TestInvalidTimesManager(TestCase):
    def test_input_validation(self):
        with self.assertRaises(NoneParamException):
            FlInvalidTimeManager(None, [])
        with self.assertRaises(NoneParamException):
            FlInvalidTimeManager(1, None)
