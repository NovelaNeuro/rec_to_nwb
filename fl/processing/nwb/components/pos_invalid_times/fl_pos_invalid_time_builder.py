from fl.processing.nwb.components.pos_invalid_times.fl_pos_invalid_times import FlPosInvalidTime
from fl.processing.tools.beartype.beartype import beartype


class FlPosInvalidTimeBuilder:

    @staticmethod
    @beartype
    def build(start_time: float, stop_time: float):
        return FlPosInvalidTime(
            start_time=start_time,
            stop_time=stop_time
        )
