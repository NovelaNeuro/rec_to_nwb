from fl.datamigration.nwb.components.invalid_times.fl_gap import FlGap

from matplotlib import pyplot

class FlInvalidTimeBuilder:
    def build(self, timestamps, data_type, period=None, unfinished_gap=None, last_timestamp=None):
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

        dist_tab = []

        for timestamp in timestamps:

            dist_tab.append(timestamp - last_timestamp)


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

        pyplot.hist(dist_tab, label=data_type, bins=1000)
        print(data_type)
        counter = 0
        for dist in dist_tab:
            if dist > period:
                counter += 1
        print('counter ' + str(counter))
        set_dist = set(dist_tab)
        print(len(set_dist))
        print(set_dist)
        pyplot.show()
        return gaps


