from unittest import TestCase

from fl.datamigration.nwb.components.analog.analog_builder import AnalogBuilder


class TestAnalogBuilder(TestCase):

    def setUp(self):
        self.data = {
            'AccelX': [[1, 1, 1, 1], [11, 11, 11, 11]],
            'AccelY': [[2, 2, 2], [22, 22, 22]]}

    def test_build(self):
        analog_builder = AnalogBuilder(data=self.data)
        behavioral_events = analog_builder.build()
        self.assertEqual(9, len(behavioral_events.time_series))
        self.assertEqual([11, 11, 11, 11], behavioral_events.time_series['AccelX'].data)
