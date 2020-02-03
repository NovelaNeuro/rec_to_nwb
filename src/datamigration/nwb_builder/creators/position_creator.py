import logging.config
import os

from pynwb.behavior import Position

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PositionCreator:

    @staticmethod
    def create_position(position_data, timestamps):
        position = Position()
        position.create_spatial_series(
            name="series",
            data=position_data,
            reference_frame="Description defining what the zero-position is",
            timestamps=timestamps
        )
        return position
