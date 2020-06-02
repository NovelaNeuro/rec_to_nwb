import numpy as np
from pynwb import NWBFile

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.nwb.components.position.time.valid.fl_pos_valid_time_builder import FlPosValidTimeBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.get_times_period_multiplier import get_times_period_multiplier


class FlPosValidTimeManager:
    """" Manage POS data and call FLPosValidTimeBuilder to create list of FLPosValidTime objects.

    Args:
        metadata (dict): Project metadata

    Methods:
        get_fl_pos_valid_times()
    """

    def __init__(self, metadata):
        self.period_multiplier = get_times_period_multiplier(metadata)

    @beartype
    def get_fl_pos_valid_times(self, nwb_content: NWBFile, gaps_margin: float = 0.000001) -> list:
        """ Manage POS data and call FlPosValidTimeBuilder for every valid gap.

        Args:
            nwb_content (NWBFile): NWBFile object with MDA timestamps inside
            gaps_margin (float): Error margin for valid gaps

        Raises:
            MissingDataException: If timestamps are empty

        Returns:
            list of FlPosValidTime objects
        """

        timestamps = self.__get_pos_timestamps(nwb_content)
        pos_period = self.__calculate_pos_period(timestamps)
        valid_times = self.__get_pos_valid_times(timestamps, pos_period, gaps_margin)
        return self.__build_pos_valid_times(valid_times)

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
        valid_intervals = [valid_time > min_valid_len for valid_time in valid_times[:, 1] - valid_times[:, 0]]
        return valid_times[valid_intervals, :]

    @staticmethod
    def __build_pos_valid_times(valid_times):
        return [FlPosValidTimeBuilder.build(gap[0], gap[1]) for gap in valid_times]


