from src.datamigration.xml_extractor import XMLExtractor


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
