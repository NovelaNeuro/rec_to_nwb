import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class HeaderLogger:

    @staticmethod
    def log_header_differences(headers_differences, rec_files_list):
        if headers_differences:
            message = 'Rec files: ' + str(rec_files_list) + ' contain inconsistent xml headers!\n'
            differences = [diff for diff in headers_differences
                           if 'systemTimeAtCreation' not in str(diff) and 'timestampAtCreation'
                           not in str(diff)]
            logger.warning('%s , %s', message, differences)
