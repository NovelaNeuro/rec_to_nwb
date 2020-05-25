import numpy as np
from pynwb import NWBFile

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.nwb.components.pos_invalid_times.fl_pos_invalid_time_builder import FlPosInvalidTimeBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlPosInvalidTimeManager:
    """" Manage POS data and call FLPosInvalidTimeBuilder to create list of FLPosInvalidTime objects.

    Methods:
        get_fl_pos_invalid_times()
    """

    def __init__(self):
        self.period_multiplier = 1.5

    @beartype
    def get_fl_pos_invalid_times(self, nwb_content: NWBFile, gaps_margin: float = 0.0001) -> list:
        """ Manage POS data and call FlPosInvalidTimeBuilder for every invalid gap.

        Args:
            nwb_content (NWBFile): NWBFile object with MDA timestamps inside
            gaps_margin (float): Error margin for invalid gaps

        Raises:
            MissingDataException: If timestamps are empty

        Returns:
            list of FlPosInvalidTime objects
        """

        timestamps = self.__get_pos_timestamps(nwb_content)
        pos_period = self.__calculate_pos_period(timestamps)
        invalid_times = self.__get_pos_invalid_times(timestamps, pos_period, gaps_margin)
        return self.__build_pos_invalid_times(invalid_times)

    @staticmethod
    def __get_pos_timestamps(nwb_content):
        timestamps = np.array(
            nwb_content.processing['behavior'].data_interfaces['position'].spatial_series['series'].timestamps
        )

        if timestamps.any():
            return timestamps
        raise MissingDataException('POS timestamp not found')

    @staticmethod
    def __calculate_pos_period(timestamps):
        number_of_invalid_records_at_start_of_a_file = 0
        number_of_invalid_records_at_end_of_a_file = 0

        first_timestamp = timestamps[0]
        last_timestamp = timestamps[-1]

        len_of_timestamps = len(timestamps)
        while not first_timestamp >= 0:
            number_of_invalid_records_at_start_of_a_file += 1
            first_timestamp = timestamps[number_of_invalid_records_at_start_of_a_file]
        while not last_timestamp >= 0:
            number_of_invalid_records_at_end_of_a_file += 1
            last_timestamp = timestamps[(-1 - number_of_invalid_records_at_end_of_a_file)]
        return (last_timestamp - first_timestamp) / \
               (len_of_timestamps - number_of_invalid_records_at_end_of_a_file -
                number_of_invalid_records_at_start_of_a_file)

    def __get_pos_invalid_times(self, timestamps, period, gaps_margin):
        min_valid_len = 3 * gaps_margin
        valid_times = self.__get_pos_valid_times(timestamps, period, gaps_margin)

        start_times = np.append(np.asarray(timestamps[0] + gaps_margin), (valid_times[:, 1] + 2 * gaps_margin))
        stop_times = np.append(valid_times[:, 0] - 2 * gaps_margin, np.asarray(timestamps[-1] - gaps_margin))

        invalid_times = (np.vstack([start_times, stop_times])).transpose()
        valid_intervals = (invalid_times[:, 1] - invalid_times[:, 0]) > min_valid_len
        return invalid_times[valid_intervals, :]

    def __get_pos_valid_times(self, timestamps, period, gaps_margin):
        min_valid_len = 3*gaps_margin
        timestamps = timestamps[~np.isnan(timestamps)]

        gaps = np.diff(timestamps) > period * self.period_multiplier
        gap_indexes = np.asarray(np.where(gaps))
        gap_start = np.insert(gap_indexes + 1, 0, 0)
        gap_end = np.append(gap_indexes, np.asarray(len(timestamps)-1))

        valid_indices = np.vstack([gap_start, gap_end]).transpose()
        valid_times = timestamps[valid_indices]
        valid_times[:, 0] = valid_times[:, 0] + gaps_margin
        valid_times[:, 1] = valid_times[:, 1] - gaps_margin
        valid_intervals = (valid_times[:, 1] - valid_times[:, 0]) > min_valid_len
        return valid_times[valid_intervals, :]

    @staticmethod
    def __build_pos_invalid_times(invalid_times):
        return [FlPosInvalidTimeBuilder.build(gap[0], gap[1]) for gap in invalid_times]




