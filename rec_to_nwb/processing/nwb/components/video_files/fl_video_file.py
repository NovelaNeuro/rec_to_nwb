from numpy.core.multiarray import ndarray
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlVideoFile:

    @beartype
    def __init__(self, name: str, timestamps: ndarray, device: int):
        self.name = name
        self.timestamps = timestamps
        self.device = device
