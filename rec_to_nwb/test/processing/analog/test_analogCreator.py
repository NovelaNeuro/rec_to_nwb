from unittest import TestCase

import numpy

from rec_to_nwb.processing.nwb.components.analog.analog_creator import AnalogCreator
from rec_to_nwb.processing.nwb.components.analog.fl_analog import FlAnalog


class TestAnalogCreator(TestCase):

    def setUp(self):
        self.data = numpy.array(
            [
                [1, 1, 1, 1],
                [2, 2, 2, 2],
                [3, 3, 3, 3],
                [4, 4, 4, 4],
                [5, 5, 5, 5],
                [6, 6, 6, 6],
                [7, 7, 7, 7],
                [8, 8, 8, 8],
                [9, 9, 9, 9],
            ]
        )

        self.timestamp = numpy.array([1, 2, 3, 4])
        self.fl_analog = FlAnalog(self.data, self.timestamp, 'description')

    def test_creator_create_analog_successfully(self):
        analog = AnalogCreator.create(self.fl_analog, 'um')
        self.assertIsNotNone(analog)
        self.assertEqual((9, 4), analog.fields['time_series']['analog'].data.shape)
        self.assertEqual(4, analog.fields['time_series']['analog'].timestamps.size)