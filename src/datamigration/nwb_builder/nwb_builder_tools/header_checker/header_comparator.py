import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class HeaderComparator:

    def __init__(self, xml_headers):
        self.xml_headers = xml_headers

    def compare(self):
        if len(self.xml_headers) > 1:
            header_1 = self.xml_headers[0]
            return all(header == header_1 for header in self.xml_headers)
        return True
