from pynwb.epoch import TimeIntervals


class PosValidTimeInjector:

    def inject_all(self, valid_times, nwb_content):
        intervals = TimeIntervals(
            name='pos_valid_times',
            description='Valid times based on pos timestamps',
        )
        for single_interval in valid_times:
            self.inject(single_interval, intervals)
        nwb_content.add_time_intervals(intervals)

    @staticmethod
    def inject(single_interval, intervals):
        intervals.add_interval(
            single_interval.start_time,
            single_interval.stop_time
        )
