from pynwb.epoch import TimeIntervals


class PosInvalidTimeInjector:

    @staticmethod
    def inject(valid_times, nwb_content):
        intervals = TimeIntervals(
            name='pos_inalid_times',
            description='Invalid times based on pos timestamps',
        )
        for interval in valid_times:
            intervals.add_interval(interval.start_time, interval.stop_time)
        nwb_content.add_time_intervals(intervals)


