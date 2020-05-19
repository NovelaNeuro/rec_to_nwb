from pynwb.epoch import TimeIntervals


class MdaInvalidTimeInjector:

    @staticmethod
    def inject(invalid_times, nwb_content):
        intervals = TimeIntervals(
            name='pos_invalid_times',
            description='Invalid times based on pos timestamps',
        )
        for interval in invalid_times:
            intervals.add_interval(interval.start_time, interval.stop_time)
        nwb_content.add_time_intervals(intervals)


