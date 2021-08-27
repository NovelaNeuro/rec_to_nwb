import logging.config
import os

import numpy as np

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(
    fname=os.path.join(str(path), os.pardir, os.pardir, 'logging.conf'),
    disable_existing_loggers=False)
logger = logging.getLogger(__name__)

NANOSECONDS_PER_SECOND = 1E9


class TimestampConverter:

    @staticmethod
    def convert_timestamps(continuous_times, timestamps):
        '''Matches the trodes timestamp index from the camera to the adjusted
        timestamps (in unix time) from the ephys recording.

        The adjusted timestamps are the ephys recoding timestamps adjusted for
        jitter from the arrival times of packets from the MCU.

        Timestamps from the camera that do not having matching timestamps from
        the ephys recording will be marked as NaN. This can happen when the
        position tracking is shut off after the ephys recording is done or
        started before the ephys recording starts.

        Parameters
        ----------
        continuous_times: ndarray, shape (2, n_ephys_time)
            From the continuous time file
            row 0: trodestime, row 1: adjusted_systime_
        timestamps: ndarray, shape (n_position_time, )
            trodes timestamps relative to camera’s timing (from pos_online.dat)

        Returns
        -------
        converted_timestamps : ndarray, shape (n_position_time,)
            Timestamps from the position tracking in terms of the adjusted
            timestamps. Also converted to seconds.

        '''
        # Find the matching timestamp index (trodestime)
        timestamp_ind = np.digitize(timestamps, continuous_times[0, 1:-1])
        converted_timestamps = (continuous_times[1, timestamp_ind] /
                                NANOSECONDS_PER_SECOND)

        # Mark timestamps not found in continuous time as NaN
        not_found = timestamps != continuous_times[0, timestamp_ind]
        converted_timestamps[not_found] = np.nan

        return converted_timestamps
