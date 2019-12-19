import os


class HeaderReader:

    def __init__(self, xml_files):
        self.xml_headers = []
        self.xml_files = xml_files

    def read_headers(self):
        for xml_file in self.xml_files:
            with open(xml_file, 'r') as content:
                self.xml_headers.append(content.read())
            os.remove(xml_file)
        return self.xml_headers
