from unittest import TestCase

from rec_to_nwb.processing.nwb.components.dio.dio_builder import DioBuilder


class TestDioBuilder(TestCase):

    def setUp(self):
        self.data = {
            'Din1': [[1, 1, 1, 1], [11, 11, 11, 11]],
            'Din2': [[2, 2, 2], [22, 22, 22]]}
        self.metadata = [
            {'name': 'Din1', 'description': 'poke1'},
            {'name': 'Din2', 'description': 'poke2'}]

    def test_build(self):
        dio_builder = DioBuilder(data=self.data,
                                 dio_metadata=self.metadata)
        behavioral_events = dio_builder.build()
        self.assertEqual(2, len(behavioral_events.time_series))
        self.assertEqual([11, 11, 11, 11], behavioral_events.time_series['Din1'].data)
        self.assertEqual('poke2', behavioral_events.time_series['Din2'].description)
