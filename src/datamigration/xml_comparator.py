import os

from src.datamigration.xml_extractor import XMLExtractor


class HeaderComparator:

    def __init__(self, rec_files):
        self.rec_files = rec_files
        self.xml_files = []

    def header_extractor(self):
        for rec_file in self.rec_files:
            temp_xml_extractor = XMLExtractor(rec_path=rec_file,
                                              xml_path=str(rec_file) + '.xml')
            temp_xml_extractor.extract_xml_from_rec_file()
            self.xml_files.append(str(rec_file) + '.xml')

    def xml_comparator(self):
        with open(self.xml_files[0]) as xml_file:
            first_xml = xml_file.read()
            return all(open(xml_file, 'r').read() == first_xml for xml_file in self.xml_files)

    def compare(self):
        self.header_extractor()
        return self.xml_comparator()

    def clean(self):
        for xml_file in self.xml_files:
            os.remove(xml_file)
