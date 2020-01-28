import logging

from src.datamigration.nwb_builder.extractors.xml_extractor import XMLExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_comparator import HeaderComparator
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_extractor import HeaderFilesExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_reader import HeaderReader
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.rec_file_finder import RecFileFinder


def check_headers_compatibility(data_path, animal_name, date):
    rec_files = RecFileFinder().find_rec_files(data_path + animal_name + '/raw')
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
                 xml_path=data_path + '/' + animal_name + '/preprocessing/' +
                          date + '/header.xml').extract_xml_from_rec_file()