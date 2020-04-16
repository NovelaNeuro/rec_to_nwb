from unittest import TestCase

import numpy as np

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.invalid_times.invalid_time_manager import InvalidTimeManager

class TestInvalidTimesManager(TestCase):
    def test_imput_validation(self):
        with self.assertRaises(NoneParamException):
            InvalidTimeManager(None, [])
        with self.assertRaises(NoneParamException):
            InvalidTimeManager(0, [])
