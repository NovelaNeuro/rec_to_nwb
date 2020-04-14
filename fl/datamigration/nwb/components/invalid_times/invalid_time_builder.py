from fl.datamigration.nwb.components.invalid_times.fl_gap import FlGap


class InvalidTimeBuilder:
    def __init__(self, sampling_rate):
        self.period = 1 / sampling_rate

    def build(self, timestamps):
        was_last_timestamp_part_of_a_gap = False
        gap_start_time, gap_stop_time = timestamps[0], timestamps[0]
        gaps = []
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
            last_timestamp = timestamp
        return gaps
