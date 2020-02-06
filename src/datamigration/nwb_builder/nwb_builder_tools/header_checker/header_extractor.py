from src.datamigration.nwb_builder.extractors.xml_extractor import XMLExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.rec_file_finder import RecFileFinder


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

    def extract_header_for_processing(self, date, animal_name, data_path):
        rec_file_finder = RecFileFinder()
        rec_files = rec_file_finder.find_rec_files((data_path
                                                    + '/' + animal_name
                                                    + '/raw/'
                                                    + date))
        rec_file_for_processing = rec_files[0]
        xml_extractor = XMLExtractor(rec_path=rec_file_for_processing,
                                     xml_path=data_path + '/' + animal_name + '/preprocessing/' + date + '/header.xml')
        xml_extractor.extract_xml_from_rec_file()
