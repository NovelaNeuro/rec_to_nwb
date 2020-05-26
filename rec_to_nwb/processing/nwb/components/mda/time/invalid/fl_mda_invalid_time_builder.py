from rec_to_nwb.processing.nwb.components.mda.time.invalid.fl_mda_invalid_time import FlMdaInvalidTime
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlMdaInvalidTimeBuilder:

    @staticmethod
    @beartype
    def build(start_time: float, stop_time: float):
        return FlMdaInvalidTime(
            start_time=start_time,
            stop_time=stop_time
        )


