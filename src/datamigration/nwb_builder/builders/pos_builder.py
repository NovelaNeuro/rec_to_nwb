from pynwb.behavior import Position


class PosBuilder:

    def __init__(self):
        pass

    @staticmethod
    def build(position_data, timestamps):
        position = Position()
        position.create_spatial_series(
            name="series",
            data=position_data,
            reference_frame="Description defining what the zero-position is",
            timestamps=timestamps
        )

        return position
