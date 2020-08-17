from unittest import TestCase
from unittest.mock import MagicMock

import numpy as np

from rec_to_nwb.processing.nwb.components.video_files.camera_sample_frame_counts.camera_sample_frame_counts_extractor import \
    CameraSampleFrameCountsExtractor
from rec_to_nwb.processing.nwb.components.video_files.camera_sample_frame_counts.camera_sample_frame_counts_manager import \
    CameraSampleFrameCountsManager


class TestSampleCountTimestampCorespondenceManager(TestCase):

    def test_sample_count_timestamp_corespondence_manager(self):
        mock_list = [[1, 10, 111], [2, 20, 222], [3, 30, 333]]
        mock_ndarray = np.ndarray(shape=(3, 2), dtype='int64')
        for i, single_row in enumerate(mock_list):
            mock_ndarray[i, 0] = single_row[1]
            mock_ndarray[i, 1] = single_row[0]
        mock_extractor = MagicMock(spec=CameraSampleFrameCountsExtractor)
        mock_extractor.files = []
        mock_extractor.extract = MagicMock(return_value=mock_ndarray)

        corespondence_manager = CameraSampleFrameCountsManager([])
        corespondence_manager.extractor = mock_extractor
        timeseries = corespondence_manager.get_timeseries()

        self.assertEqual(timeseries.data[0], 10)
        self.assertEqual(timeseries.data[1], 20)
        self.assertEqual(timeseries.data[2], 30)
        self.assertEqual(timeseries.timestamps[0], 1)
        self.assertEqual(timeseries.timestamps[1], 2)
        self.assertEqual(timeseries.timestamps[2], 3)