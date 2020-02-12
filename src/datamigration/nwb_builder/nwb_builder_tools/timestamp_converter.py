import logging.config
import os

import numpy as np

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TimestampConverter:
    @staticmethod
    def convert_timestamps(continuous_time_dict, timestamps):
        converted_timestamps = np.ndarray([np.shape(timestamps)[0], ], dtype="float64")
        for i in range(np.shape(timestamps)[0]):
            key = str(timestamps[i])
            try:
                value = continuous_time_dict[key]
                converted_timestamps[i] = float(value) / 1E9
            except KeyError as error:
                message = 'Following key: ' + str(key) + ' does not exist!' + str(error)
                logger.exception(message)
                converted_timestamps[i] = float('nan')
        return converted_timestamps
