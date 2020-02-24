from src.datamigration.header.xml_extractor import XMLExtractor


class HeaderFilesExtractor:

    def __init__(self):
        self.xml_files = []

    def extract_headers_from_rec_files(self, rec_files):
        for rec_file in rec_files:
            temp_xml_extractor = XMLExtractor(rec_path=rec_file,
                                              xml_path=str(rec_file) + '_header' + '.xml')
            temp_xml_extractor.extract_xml_from_rec_file()
            self.xml_files.append(str(rec_file) + '_header' + '.xml')
        return self.xml_files
