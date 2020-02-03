import logging.config
import os

from src.datamigration.nwb_builder.extractors.xml_extractor import XMLExtractor

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class HeaderFilesExtractor:

    def __init__(self):
        self.xml_files = []

    def extract(self, rec_files):
        for rec_file in rec_files:
            temp_xml_extractor = XMLExtractor(rec_path=rec_file,
                                              xml_path=str(rec_file) + '.xml')
            temp_xml_extractor.extract_xml_from_rec_file()
            self.xml_files.append(str(rec_file) + '.xml')
        return self.xml_files
