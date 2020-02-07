import os
from xmldiff import main


class HeaderReader:

    def __init__(self, xml_files):
        self.xml_headers = []
        self.xml_files = xml_files
        self.headers_differences = []
        first_xml_file = xml_files[0]
        for xml_file in xml_files:
            self.headers_differences += main.diff_files(first_xml_file, xml_file)

    def read_headers(self):
        for xml_file in self.xml_files:
            with open(xml_file, 'r') as content:
                self.xml_headers.append(content.read())
        return self.xml_headers
