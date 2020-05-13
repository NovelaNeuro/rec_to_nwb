from pynwb.epoch import TimeIntervals


class PosValidTimeInjector:

    @staticmethod
    def inject(valid_times, nwb_content):
        intervals = TimeIntervals(
            name='pos_valid_times',
            description='Valid times based on pos timestamps',
        )
        for interval in valid_times:
            intervals.add_interval(interval.start_time, interval.stop_time)
        nwb_content.add_time_intervals(intervals)


