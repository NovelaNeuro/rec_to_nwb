from unittest import TestCase

import numpy as np

from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_builder import FlInvalidTimeBuilder


class TestInvalidTimesBuilder(TestCase):
    def setUp(self):
        self.sampling_rate = 1
        self.fl_invalid_time_builder = FlInvalidTimeBuilder()

    def test_all_data_valid(self):
        timestamps = np.ndarray(dtype='float64', shape=(5,))
        for i in range(5):
            timestamps[i] = 0.8 * i
        self.assertEqual(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate), [])

    def test_all_data_invalid(self):
        timestamps = np.ndarray(dtype='float64', shape=(5,))
        for i in range(5):
            timestamps[i] = 1.1 * i
        self.assertEqual(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)[0].start_time, 0)
        self.assertEqual(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)[0].stop_time, 4.4)

    def test_gap_in_the_middle(self):
        timestamps = np.ndarray(dtype='float64', shape=(15,))
        for i in range(5):
            timestamps[i] = 0.9 * i
        for i in range(5):
            timestamps[i + 5] = 4.5 + 1.1 * i
        for i in range(5):
            timestamps[i + 10] = 10 + 0.9 * i

        self.assertEqual(len(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)), 1)
        self.assertEqual(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)[0].start_time, 4.5)
        self.assertEqual(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)[0].stop_time, 10)

    def test_multiple_gaps(self):
        timestamps = np.ndarray(dtype='float64', shape=(15,))
        for i in range(5):
            timestamps[i] = 1.1 * i
        for i in range(5):
            timestamps[i + 5] = 5.5 + 0.9 * i
        for i in range(5):
            timestamps[i + 10] = 10 + 1.1 * i

        self.assertEqual(len(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)), 2)
        self.assertEqual(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)[0].start_time, 0)
        self.assertEqual(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)[0].stop_time, 5.5)
        self.assertEqual(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)[1].start_time, 10)
        self.assertEqual(self.fl_invalid_time_builder.build(timestamps, 'test', self.sampling_rate)[1].stop_time, 14.4)
