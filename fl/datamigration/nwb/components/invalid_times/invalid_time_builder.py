from fl.datamigration.nwb.components.invalid_times.fl_gap import FlGap


class InvalidTimeBuilder:
    def __init__(self, sampling_rate):
        self.period = 1 / float(sampling_rate)

    def build(self, timestamps, unfinished_gap=None, last_timestamp=None):
        gap_start_time, gap_stop_time = timestamps[0], timestamps[0]
        gaps = []
        if unfinished_gap:
            was_last_timestamp_part_of_a_gap = True
            gap_start_time = unfinished_gap.start_time
            last_timestamp = gap_start_time
        else:
            was_last_timestamp_part_of_a_gap = False
            if not last_timestamp:
                last_timestamp = timestamps[0]

        for timestamp in timestamps:
            if not was_last_timestamp_part_of_a_gap:
                if last_timestamp + self.period < timestamp:
                    gap_start_time = last_timestamp
                    was_last_timestamp_part_of_a_gap = True
            else:
                if last_timestamp + self.period > timestamp:
                    gap_stop_time = last_timestamp
                    was_last_timestamp_part_of_a_gap = False
                    gaps.append(FlGap(gap_start_time, gap_stop_time))
                elif timestamp == timestamps[-1]:
                    gap_stop_time = timestamp
                    gaps.append(FlGap(gap_start_time, gap_stop_time))
            last_timestamp = timestamp
        return gaps
