from pynwb.behavior import Position


class PositionCreator:

    @staticmethod
    def create_position(position_data, timestamps):
        position = Position()
        position.create_spatial_series(
            name='series',
            data=position_data,
            reference_frame='Description defining what the zero-position is',
            timestamps=timestamps
        )
        return position
