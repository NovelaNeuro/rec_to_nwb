import numpy as np
from pynwb import NWBFile

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.nwb.components.mda.time.valid.fl_mda_valid_time_builder import FlMdaValidTimeBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.get_times_period_multiplier import get_times_period_multiplier


class FlMdaValidTimeManager:
    """" Manage MDA data and call FLMdaValidTimeBuilder to create list of FLMdaValidTime objects.

    Args:
        sampling_rate (float): Sampling rate of MDA data
        metadata (dict): Project metadata

    Methods:
        get_fl_mda_valid_times()
    """

    @beartype
    def __init__(self, sampling_rate: float, metadata: dict):
        self.sampling_rate = sampling_rate

        self.period_multiplier = get_times_period_multiplier(metadata)

    @beartype
    def get_fl_mda_valid_times(self, nwb_content: NWBFile, gaps_margin: float = 0.000001) -> list:
        """ Manage MDA data and call FlMdaValidTimeBuilder for every valid gap.

        Args:
            nwb_content (NWBFile): NWBFile object with MDA timestamps inside
            gaps_margin (float): Error margin for valid gaps

        Raises:
            MissingDataException: If timestamps are empty

        Returns:
            list of FlMdaValidTime objects
        """

        timestamps = self.__get_mda_timestamps(nwb_content)
        period = 1 / self.sampling_rate
        valid_times = self.__get_mda_valid_times(timestamps, period, gaps_margin)
        return self.__build_mda_valid_times(valid_times)

    @staticmethod
    def __get_mda_timestamps(nwb_content):
        timestamps = np.array(
            nwb_content.acquisition['e-series'].timestamps
        )

        if timestamps.any():
            return timestamps
        raise MissingDataException('MDA timestamp not found')

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
        valid_intervals = [valid_time > min_valid_len for valid_time in valid_times[:, 1] - valid_times[:, 0]]
        return valid_times[valid_intervals, :]

    @staticmethod
    def __build_mda_valid_times(valid_times):
        return [FlMdaValidTimeBuilder.build(gap[0], gap[1]) for gap in valid_times]
