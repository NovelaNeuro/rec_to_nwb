"""Class that stores the position information"""


class FlPosition:
    """Stores the position information"""

    def __init__(self, position_data, column_labels, timestamps, conversion):
        self.position_data = position_data
        self.column_labels = column_labels
        self.timestamps = timestamps
        self.conversion = conversion
