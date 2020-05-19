from unittest import TestCase

from rec_to_nwb.processing.nwb.components.dio.dio_builder import DioBuilder


class TestDioBuilder(TestCase):

    def setUp(self):
        self.data = {
            'Din1': [[1, 1, 1, 1], [11, 11, 11, 11]],
            'Din2': [[2, 2, 2], [22, 22, 22]]}
        self.metadata = [
            {'name': 'poke1', 'description': 'Din1'},
            {'name': 'poke2', 'description': 'Din2'}]

    def test_build(self):
        dio_builder = DioBuilder(data=self.data,
                                 dio_metadata=self.metadata)
        behavioral_events = dio_builder.build()
        self.assertEqual(2, len(behavioral_events.time_series))
        self.assertEqual([11, 11, 11, 11], behavioral_events.time_series['poke1'].data)
        self.assertEqual('Din2', behavioral_events.time_series['poke2'].description)
