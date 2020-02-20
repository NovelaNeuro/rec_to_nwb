import logging.config
import os

import numpy as np

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TimestampConverter:

    @staticmethod
    def convert_timestamps(continuous_time_dict, timestamps):
        # ToDO shape = len(timestamp)
        converted_timestamps = np.ndarray(shape=[np.shape(timestamps)[0], ], dtype="float64")
        # ToDo for counter, timestamp in enumerate(timestamps):
        for i in range(np.shape(timestamps)[0]):
            key = str(timestamps[i])
            value = continuous_time_dict.get(key, float('nan')) / 1E9
            if np.isnan(value):
                message = 'Following key: ' + str(key) + ' does not exist in continioustime dictionary!'
                logger.exception(message)
            converted_timestamps[i] = value
        return converted_timestamps
