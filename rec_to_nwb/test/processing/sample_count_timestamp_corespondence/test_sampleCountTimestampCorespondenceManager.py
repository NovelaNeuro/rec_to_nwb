from unittest import TestCase
from unittest.mock import MagicMock

import numpy as np

from rec_to_nwb.processing.nwb.components.sample_count_timestamp_corespondence.sample_count_timestamp_corespondence_extractor import \
    SampleCountTimestampCorespondenceExtractor
from rec_to_nwb.processing.nwb.components.sample_count_timestamp_corespondence.sample_count_timestamp_corespondence_manager import \
    SampleCountTimestampCorespondenceManager


class TestSampleCountTimestampCorespondenceManager(TestCase):

    def test_sample_count_timestamp_corespondence_manager(self):
        mock_list = [[1, 10, 11, 111], [2, 20, 21, 222], [3, 30, 31, 333]]
        mock_ndarray = np.ndarray(shape=(3, 2), dtype='int64')
        for i, single_row in enumerate(mock_list):
            mock_ndarray[i, 0] = single_row[0]
            mock_ndarray[i, 1] = single_row[3]
        mock_extractor = MagicMock(spec=SampleCountTimestampCorespondenceExtractor)
        mock_extractor.files = []
        mock_extractor.extract = MagicMock(return_value=mock_ndarray)

        corespondence_manager = SampleCountTimestampCorespondenceManager([])
        corespondence_manager.extractor = mock_extractor
        timeseries = corespondence_manager.get_timeseries()

        self.assertEqual(timeseries.data[0], 1)
        self.assertEqual(timeseries.data[1], 2)
        self.assertEqual(timeseries.data[2], 3)
        self.assertEqual(timeseries.timestamps[0], 111)
        self.assertEqual(timeseries.timestamps[1], 222)
        self.assertEqual(timeseries.timestamps[2], 333)
