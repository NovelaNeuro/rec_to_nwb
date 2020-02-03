import logging.config
import os

from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_comparator import HeaderComparator
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_extractor import HeaderFilesExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_reader import HeaderReader

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class HeaderChecker:

    def __init__(self, rec_files_list):
        self.rec_files_list = rec_files_list
        header_extractor = HeaderFilesExtractor()
        self.headers = header_extractor.extract(rec_files_list)
        self.header_reader = HeaderReader(self.headers)
        self.xml_headers = self.header_reader.read_headers()
        self.comparator = HeaderComparator(self.xml_headers)

    def log_headers_compatibility(self):
        if not self.comparator.compare():
            message = 'Rec files: ' + str(self.rec_files_list) + ' contain incosistent xml headers!'
            differences = [diff for diff in self.header_reader.headers_differences
                           if 'systemTimeAtCreation' not in str(diff) and 'timestampAtCreation'
                           not in str(diff)]
            logger.warning(message, differences, )
