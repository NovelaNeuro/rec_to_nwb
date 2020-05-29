import numpy as np
from pynwb import NWBFile

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.nwb.components.mda.time.invalid.fl_mda_invalid_time_builder import FlMdaInvalidTimeBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlMdaInvalidTimeManager:
    """" Manage MDA data and call FLMdaInvalidTimeBuilder to create list of FLMdaInvalidTime objects.

    Args:
        sampling_rate (float): Sampling rate of MDA data

    Methods:
        get_fl_mda_invalid_times()
    """

    @beartype
    def __init__(self, sampling_rate: float):
        self.sampling_rate = sampling_rate

        self.period_multiplier = 1.5

    @beartype
    def get_fl_mda_invalid_times(self, nwb_content: NWBFile, gaps_margin: float = 0.0001) -> list:
        """ Manage MDA data and call FlMdaInvalidTimeBuilder for every invalid gap.

        Args:
            nwb_content (NWBFile): NWBFile object with MDA timestamps inside
            gaps_margin (float): Error margin for invalid gaps

        Raises:
            MissingDataException: If timestamps are empty

        Returns:
            list of FlMdaInvalidTime objects
        """

        timestamps = self.__get_mda_timestamps(nwb_content)
        period = 1 / self.sampling_rate
        invalid_times = self.__get_mda_invalid_times(timestamps, period, gaps_margin)
        return self.__build_mda_invalid_times(invalid_times)

    @staticmethod
    def __get_mda_timestamps(nwb_content):
        timestamps = np.array(
            nwb_content.acquisition['e-series'].timestamps
        )

        if timestamps.any():
            return timestamps
        raise MissingDataException('MDA timestamp not found')

    def __get_mda_invalid_times(self, timestamps, period, gaps_margin):
        min_valid_len = 3 * gaps_margin
        valid_times = self.__get_mda_valid_times(timestamps, period, gaps_margin)

        start_times = np.append(np.asarray(timestamps[0] + gaps_margin), (valid_times[:, 1] + 2 * gaps_margin))
        stop_times = np.append(valid_times[:, 0] - 2 * gaps_margin, np.asarray(timestamps[-1] - gaps_margin))

        invalid_times = (np.vstack([start_times, stop_times])).transpose()
        valid_intervals = (invalid_times[:, 1] - invalid_times[:, 0]) > min_valid_len
        return invalid_times[valid_intervals, :]

    def __get_mda_valid_times(self, timestamps, period, gaps_margin):
        min_valid_len = 3 * gaps_margin
        timestamps = timestamps[~np.isnan(timestamps)]

        gaps = np.diff(timestamps) > period * self.period_multiplier
        gap_indexes = np.asarray(np.where(gaps))
        gap_start = np.insert(gap_indexes + 1, 0, 0)
        gap_end = np.append(gap_indexes, np.asarray(len(timestamps) - 1))

        valid_indices = np.vstack([gap_start, gap_end]).transpose()
        valid_times = timestamps[valid_indices]
        valid_times[:, 0] = valid_times[:, 0] + gaps_margin
        valid_times[:, 1] = valid_times[:, 1] - gaps_margin
        valid_intervals = (valid_times[:, 1] - valid_times[:, 0]) > min_valid_len
        return valid_times[valid_intervals, :]

    @staticmethod
    def __build_mda_invalid_times(invalid_times):
        return [FlMdaInvalidTimeBuilder.build(gap[0], gap[1]) for gap in invalid_times]
