from unittest import TestCase
import numpy

from fl.datamigration.nwb.components.analog.fl_analog import FlAnalog
from fl.datamigration.nwb.components.analog.analog_creator import AnalogCreator


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
        fl_analog = FlAnalog(self.data, self.timestamp)

        self.analog_creator = AnalogCreator(fl_analog)

    def test_building(self):
        analog = self.analog_creator.create()
        self.assertIsNotNone(analog)
        self.assertEqual((9, 4), analog.fields['time_series']['Analog'].data.shape)
        self.assertEqual(4, analog.fields['time_series']['Analog'].timestamps.size)