from pynwb.behavior import Position


class PositionCreator:

    @classmethod
    def create_position(cls,position_data, timestamps):
        position = Position()
        position.create_spatial_series(
            name="series",
            data=position_data,
            reference_frame="Description defining what the zero-position is",
            timestamps=timestamps
        )
        return position
