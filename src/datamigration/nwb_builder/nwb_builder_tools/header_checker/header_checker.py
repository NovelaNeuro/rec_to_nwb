import logging

from src.datamigration.nwb_builder.extractors.xml_extractor import XMLExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_comparator import HeaderComparator
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_extractor import HeaderFilesExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_reader import HeaderReader
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.rec_file_finder import RecFileFinder


class HeaderChecker:

    def __init__(self, data_path, animal_name, date):
        self.data_path = data_path
        self.animal_name = animal_name
        self.date = date

    def check_headers_compatibility(self):
        rec_files = RecFileFinder().find_rec_files(self.data_path + self.animal_name + '/raw')
        header_extractor = HeaderFilesExtractor()
        xml_files = header_extractor.extract(rec_files)
        header_reader = HeaderReader(xml_files)
        xml_headers = header_reader.read_headers()
        comparator = HeaderComparator(xml_headers)
        if not comparator.compare():
            message = 'Rec files: ' + str(rec_files) + ' contain incosistent xml headers!'
            differences = [diff for diff in header_reader.headers_differences
                           if 'systemTimeAtCreation' not in str(diff) and 'timestampAtCreation'
                           not in str(diff)]
            logging.warning(message, differences, )
            with open('headers_comparission_log.log', 'w') as headers_log:
                headers_log.write(str(message + '\n'))
                headers_log.write(str(differences))

        XMLExtractor(rec_path=rec_files[0],
                     xml_path=self.data_path + '/' + self.animal_name + '/preprocessing/'
                               + self.date + '/header.xml').extract_xml_from_rec_file()