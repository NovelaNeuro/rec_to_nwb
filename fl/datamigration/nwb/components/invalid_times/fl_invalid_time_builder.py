from fl.datamigration.nwb.components.invalid_times.fl_gap import FlGap


class InvalidTimeBuilder:
    def build(self, timestamps, data_type, sampling_rate=None, unfinished_gap=None, last_timestamp=None):
        if(data_type == 'pos'):
            period = self.__calculate_pos_period(timestamps)
        else:
            period = 1 / float(sampling_rate)
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
                if last_timestamp + period < timestamp:
                    gap_start_time = last_timestamp
                    was_last_timestamp_part_of_a_gap = True
            else:
                if last_timestamp + period > timestamp:
                    gap_stop_time = last_timestamp
                    was_last_timestamp_part_of_a_gap = False
                    gaps.append(FlGap(gap_start_time, gap_stop_time, data_type))
                elif timestamp == timestamps[-1]:
                    gap_stop_time = timestamp
                    gaps.append(FlGap(gap_start_time, gap_stop_time, data_type))
            last_timestamp = timestamp
        return gaps

    def __calculate_pos_period(self, timestamps):
        number_of_invalid_records_at_start_of_a_file = 0
        number_of_invalid_records_at_end_of_a_file = 0
        first_timestamp = timestamps[0]
        last_timestamp = timestamps[-1]
        while not first_timestamp >= 0:
            number_of_invalid_records_at_start_of_a_file += 1
            first_timestamp = timestamps[number_of_invalid_records_at_start_of_a_file]
        while not last_timestamp >= 0:
            number_of_invalid_records_at_end_of_a_file += 1
            last_timestamp = timestamps[(-1 - number_of_invalid_records_at_end_of_a_file)]
        return (last_timestamp-first_timestamp) /\
               (len(timestamps - number_of_invalid_records_at_end_of_a_file -
                    number_of_invalid_records_at_start_of_a_file))
