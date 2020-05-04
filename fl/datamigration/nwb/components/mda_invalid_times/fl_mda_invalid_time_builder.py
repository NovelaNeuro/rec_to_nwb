from fl.datamigration.nwb.components.mda_invalid_times.fl_mda_invalid_times import FlMdaInvalidTime
from fl.datamigration.tools.beartype.beartype import beartype


class FlMdaInvalidTimeBuilder:

    @staticmethod
    @beartype
    def build(start_time: float, stop_time: float):
        return FlMdaInvalidTime(
            start_time=start_time,
            stop_time=stop_time
        )


