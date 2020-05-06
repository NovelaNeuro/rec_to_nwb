from fldatamigration.processing.tools.beartype.beartype import beartype


class FlPosInvalidTime:

    @beartype
    def __init__(self, start_time: float, stop_time: float):
        self.start_time = start_time
        self.stop_time = stop_time
