import logging.config
import os

import numpy as np

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TimestampConverter:

    @staticmethod
    def convert_timestamps(continuous_times, timestamps):
        converted_timestamps = np.ndarray(shape=[len(timestamps), ], dtype="float64")
        # look up the timestamps in the first colum of  continuous_times
        timestamp_ind = np.searchsorted(continuous_times[:,0], timestamps)
        converted_timestamps = continuous_times[timestamp_ind,1] / 1E9
        # get rid of any that are not exact
        not_found = timestamps != continuous_times[timestamp_ind,0]
        print(f'in Timestamp Converter: {len(not_found)} timestamps not found in continuous time file')
        converted_timestamps[not_found] = np.nan
        return converted_timestamps
        #old code
        # for i, timestamp in enumerate(timestamps):
        #     key = str(timestamp)
        #     value = continuous_time_dict.get(key, float('nan')) / 1E9
        #     if np.isnan(value):
        #         message = 'Following key: ' + str(key) + ' does not exist in continioustime dictionary!'
        #         logger.exception(message)
        #     converted_timestamps[i] = value
        # return converted_timestamps
