import os
import unittest
from datetime import datetime

from fl.datamigration.nwb.common.session_time_extractor import SessionTimeExtractor
from fl.datamigration.tools.dataset import Dataset

path = os.path.dirname(os.path.abspath(__file__))


class TestSessionTimeExtractor(unittest.TestCase):

    def test_get_session_start_time_result(self):
        dataset1 = Dataset(1)
        dataset1.data = {'time': str(path) + '/res/continuoustime_sample'}
        session_time_extractor = SessionTimeExtractor(
            datasets=[dataset1],
            animal_name='beans',
            date='20200616',
            dataset_names=['06_w1']
        )
        session_start_time = session_time_extractor.get_session_start_time()
        self.assertIsNotNone(session_start_time)
        self.assertIsInstance(session_start_time, datetime)
        self.assertEqual(datetime.timestamp(session_start_time), 1563488986885/1E3)

