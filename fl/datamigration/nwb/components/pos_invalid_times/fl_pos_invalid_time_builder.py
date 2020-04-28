from fl.datamigration.nwb.components.pos_invalid_times.fl_pos_invalid_times import FlPosInvalidTime


class FlPosInvalidTimeBuilder:
    
    @staticmethod
    def build(start_time, stop_time):
        return FlPosInvalidTime(
            start_time=start_time,
            stop_time=stop_time
        )
