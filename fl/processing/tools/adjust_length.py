import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def adjust_extension_length(rel_x, extension, msg):
    diff_in_length = len(rel_x) - len(extension)

    if diff_in_length == 0:
        return extension
    if diff_in_length > 0:
        for _ in range(diff_in_length):
            extension.append(0.0)

        message = 'Metadata are not compatible for electrodes! ' + str(
            diff_in_length) + ' elements in ' + msg + ' were populated by "0.0" '
        logger.exception(message)

        return extension

    message = 'Metadata are not compatible for electrodes! ' + str(
        diff_in_length * (-1)) + ' elements in ' + msg + ' were cutted off '
    logger.exception(message)

    return extension[:diff_in_length]
