import numpy as np

from rec_to_nwb.processing.nwb.components.mda_invalid_times.fl_mda_invalid_time_builder import FlMdaInvalidTimeBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype


# ToDo delete extractor used before
# ToDo change tests if it will work

class FlMdaInvalidTimeManager:

    @beartype
    def __init__(self, sampling_rate: float):
        self.sampling_rate = sampling_rate

        self.period_multiplier = 1.5
    #     ToDo Period should be stored in NWBFileBuilder / metadata.yml

    @beartype
    def get_fl_mda_invalid_times(self, nwb_content, eps: float =0.0001) -> list:
        timestamps = self.__get_timestamps(nwb_content)
        period = 1E9 / self.sampling_rate
        invalid_times = self.__get_mda_invalid_times(timestamps, period, eps)
        return self.__build_mda_invalid_times(invalid_times)

    @staticmethod
    def __get_timestamps(nwb_content):
        return np.array(nwb_content.acquisition['e-series'].timestamps)
    # ToDo hardcoded place of mda? e-series

    def __get_mda_invalid_times(self, timestamps, period, eps):
        min_valid_len = 3 * eps
        valid_times = self.__get_mda_valid_times(timestamps, period, eps)

        start_times = np.append(np.asarray(timestamps[0] + eps), (valid_times[:, 1] + 2 * eps))
        stop_times = np.append(valid_times[:, 0] - 2 * eps, np.asarray(timestamps[-1] - eps))

        invalid_times = (np.vstack([start_times, stop_times])).transpose()
        valid_intervals = (invalid_times[:, 1] - invalid_times[:, 0]) > min_valid_len
        return invalid_times[valid_intervals, :]

    def __get_mda_valid_times(self, timestamps, period, eps):
        min_valid_len = 3*eps
        timestamps = timestamps[~np.isnan(timestamps)]

        gaps = np.diff(timestamps) > period * self.period_multiplier
        gap_indexes = np.asarray(np.where(gaps))
        gap_start = np.insert(gap_indexes + 1, 0, 0)
        gap_end = np.append(gap_indexes, np.asarray(len(timestamps)-1))

        valid_indices = np.vstack([gap_start, gap_end]).transpose()
        valid_times = timestamps[valid_indices]
        valid_times[:, 0] = valid_times[:, 0] + eps
        valid_times[:, 1] = valid_times[:, 1] - eps
        valid_intervals = (valid_times[:, 1] - valid_times[:, 0]) > min_valid_len
        return valid_times[valid_intervals, :]

    @staticmethod
    def __build_mda_invalid_times(invalid_times):
        return [FlMdaInvalidTimeBuilder.build(gap[0], gap[1]) for gap in invalid_times]