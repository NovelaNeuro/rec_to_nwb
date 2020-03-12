from unittest import TestCase
import numpy

from fl.datamigration.nwb.components.analog.analog_builder import AnalogBuilder


class TestFlApparatusExtractor(TestCase):

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

        self.analog_builder = AnalogBuilder(self.data, self.timestamp)

    def test_building(self):
        analog = self.analog_builder.build()
        self.assertIsNotNone(analog)
        self.assertEqual((9, 4), analog.fields['time_series']['Analog'].data.shape)
        self.assertEqual(4, analog.fields['time_series']['Analog'].timestamps.size)