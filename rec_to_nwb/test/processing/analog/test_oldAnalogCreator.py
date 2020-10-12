from unittest import TestCase

import numpy
from rec_to_nwb.processing.nwb.components.analog.old_analog_creator import OldAnalogCreator
from rec_to_nwb.processing.nwb.components.analog.old_fl_analog import OldFlAnalog


class TestOldAnalogCreator(TestCase):

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

        self.timestamp = numpy.array([])
        self.old_fl_analog = OldFlAnalog(self.data, self.timestamp, 'description')

    def test_creator_create_analog_successfully(self):
        old_analog = OldAnalogCreator.create(self.old_fl_analog, 'um')
        self.assertIsNotNone(old_analog)
        self.assertEqual((9, 4), old_analog.fields['time_series']['analog'].data.shape)
        self.assertEqual(0, old_analog.fields['time_series']['analog'].timestamps.size)
