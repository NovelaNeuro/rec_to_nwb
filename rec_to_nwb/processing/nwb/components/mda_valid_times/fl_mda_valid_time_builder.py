from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlMdaValidTimeBuilder:

    @staticmethod
    @beartype
    def build(start_time: float, stop_time: float):
        return FlMdaValidTime(
            start_time=start_time,
            stop_time=stop_time
        )
