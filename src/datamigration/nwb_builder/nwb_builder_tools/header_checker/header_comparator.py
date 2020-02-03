class HeaderComparator:

    def __init__(self, xml_headers):
        self.xml_headers = xml_headers

    def compare(self):
        if len(self.xml_headers) > 1:
            header_1 = self.xml_headers[0]
            return all(header == header_1 for header in self.xml_headers)
        return True
