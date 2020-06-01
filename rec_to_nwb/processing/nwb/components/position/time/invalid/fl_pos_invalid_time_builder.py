from rec_to_nwb.processing.nwb.components.position.time.invalid.fl_pos_invalid_time import FlPosInvalidTime
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlPosInvalidTimeBuilder:

    @staticmethod
    @beartype
    def build(start_time: float, stop_time: float):
        return FlPosInvalidTime(
            start_time=start_time,
            stop_time=stop_time
        )
