import unittest
from unittest.mock import patch
from fl.datamigration.nwb.common.session_time_extractor import SessionTimeExtractor


class TestSessionTimeExtractor(unittest.TestCase):

    @staticmethod
    def fake_read_continuous_time(*args, **kwargs):
        return {'data': [(1234, 1582199576000), (545353, 1582099345600)]}

    @patch.object(SessionTimeExtractor, '__read_continuous_time', new=fake_read_continuous_time)
    def test_get_session_start_time_result(self):
        session_time_extractor = SessionTimeExtractor(
            datasets='datasets',
            animal_name='dwarf',
            date='begin',
            dataset_names='420'
        )
        session_start_time = session_time_extractor.get_session_start_time()
        print(session_start_time)
        self.assertTrue(1)