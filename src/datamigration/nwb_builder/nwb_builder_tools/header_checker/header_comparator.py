from xmldiff import main


class HeaderComparator:

    def __init__(self, xml_headers):
        self.xml_headers = xml_headers

    def compare(self):
        headers_differences = []
        first_xml_file = self.xml_headers[0]
        for xml_file in self.xml_headers:
            headers_differences += main.diff_files(first_xml_file, xml_file)
        return headers_differences