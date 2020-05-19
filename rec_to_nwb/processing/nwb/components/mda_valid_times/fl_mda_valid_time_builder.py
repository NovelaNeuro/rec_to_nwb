from rec_to_nwb.processing.nwb.components.mda_valid_times.fl_mda_valid_times import FlMdaValidTime
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlMdaValidTimeBuilder:

    @staticmethod
    @beartype
    def build(start_time: float, stop_time: float):
        return FlMdaValidTime(start_time, stop_time)


