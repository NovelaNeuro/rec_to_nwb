from fl.datamigration.nwb.components.invalid_times.fl_gap import FlGap


class FlInvalidTimeBuilder:
    @staticmethod
    def build(start_time, stop_time):
        return FlGap(start_time=start_time, stop_time=stop_time)


