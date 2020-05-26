from rec_to_nwb.processing.nwb.components.position.time.valid.fl_pos_valid_time import FlPosValidTime
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlPosValidTimeBuilder:

    @staticmethod
    @beartype
    def build(start_time: float, stop_time: float):
        return FlPosValidTime(
            start_time=start_time,
            stop_time=stop_time
        )
