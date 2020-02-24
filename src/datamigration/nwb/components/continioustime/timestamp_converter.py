import logging.config
import os

import numpy as np

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TimestampConverter:

    @staticmethod
    def convert_timestamps(continuous_time_dict, timestamps):
        converted_timestamps = np.ndarray(shape=[len(timestamps), ], dtype="float64")
        for i, timestamp in enumerate(timestamps):
            key = str(timestamp)
            value = continuous_time_dict.get(key, float('nan')) / 1E9
            if np.isnan(value):
                message = 'Following key: ' + str(key) + ' does not exist in continioustime dictionary!'
                logger.exception(message)
            converted_timestamps[i] = value
        return converted_timestamps
