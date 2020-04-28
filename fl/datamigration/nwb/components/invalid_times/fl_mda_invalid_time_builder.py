from fl.datamigration.nwb.components.invalid_times.fl_mda_invalid_times import FlMdaInvalidTime


class FlMdaInvalidTimeBuilder:
    @staticmethod
    def build(start_time, stop_time):
        return FlMdaInvalidTime(start_time=start_time, stop_time=stop_time)


