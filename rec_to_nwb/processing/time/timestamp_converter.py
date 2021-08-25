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
        '''
        continuous_times: (2, T) numpy array, where T is the number of timepoints
                        row 0: trodestime, row 1: adjusted_systime
        timestamps: trodes timestamps relative to camera’s timing (from pos)
        '''
        # add values at the end of continuous_times to make sure all values are within the range
        max_vals = np.asarray(
            [[np.iinfo(np.int64).max], [np.iinfo(np.int64).max]], dtype=np.int64)
        continuous_times = np.hstack((continuous_times, max_vals))

        # look up the timestamps in the first row of continuous_times
        timestamp_ind = np.searchsorted(continuous_times[0, :], timestamps)
        converted_timestamps = (continuous_times[1, timestamp_ind] /
                                NANOSECONDS_PER_SECOND)

        # get rid of any that are not exact
        not_found = timestamps != continuous_times[0, timestamp_ind]
        #print(f'in Timestamp Converter: {sum(not_found)} timestamps not found in continuous time file')
        converted_timestamps[not_found] = np.nan
        return converted_timestamps

        # old code
        # converted_timestamps = np.ndarray(shape=[len(timestamps), ], dtype="float64")
        # for i, timestamp in enumerate(timestamps):
        #     key = str(timestamp)
        #     value = continuous_time_dict.get(key, float('nan')) / 1E9
        #     if np.isnan(value):
        #         message = 'Following key: ' + str(key) + ' does not exist in continioustime dictionary!'
        #         logger.exception(message)
        #     converted_timestamps[i] = value
        # return converted_timestamps
