import logging

class XMLExtractor:

    rec_path = ''
    xml_path = ''

    def __init__(self, rec_path='../data/REC_sample.xml', xml_path='../data/output.xml'):
        self.rec_path = rec_path
        self.xml_path = xml_path

    def extract_xml_from_rec_file(self):
        with open(self.rec_path, 'rb') as rec_file:
            with open(self.xml_path, 'w+') as xml_file:
                b = '</Configuration>\n'.encode()
                for line in rec_file:
                    xml_file.write(line.decode())
                    if line.find(b) != -1:
                        break

    def read_xml_from_rec_file(self):
        with open(self.rec_path, 'rb') as rec_file:
            b = '</Configuration>\n'.encode()
            for line in rec_file:
                logging.info(line)
                if line.find(b) != -1:
                    break

    def read_xml_from_xml_file(self):
        with open(self.xml_path, 'rb') as xml_file:
            for line in xml_file:
                logging.info(line)

    def set_rec_path(self, rec_path):
        self.rec_path = rec_path


    def set_xml_path(self, xml_path):
        self.xml_path = xml_path

    def get_rec_path(self):
        return self.rec_path

    def get_xml_path(self):
        return self.xml_path
