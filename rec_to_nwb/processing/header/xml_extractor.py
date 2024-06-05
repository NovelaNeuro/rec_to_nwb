""" Module to extract XML from REC file, read it and validate

Class:
    XMLExtractor()
"""


import logging

import defusedxml.cElementTree as ElementTree
from xmlschema import XMLSchema


class XMLExtractor:
    """ Class to extract XML file from REC file, read XML, validate XML with XSD file

    Methods:
        extract_xml_from_rec_file()
        read_xml_from_rec_file()
        read_xml_from_xml_file()
        set_rec_path()
        set_xml_path()
        get_rec_path()
        get_xml_path()
        is_valid()
    """
    rec_path = ''
    xml_path = ''
    xsd_path = ''

    def __init__(self,
                 rec_path='../data/REC_sample.xml',
                 xml_path='../data/output.xml',
                 xsd_path=None):
        self.rec_path = rec_path
        self.xml_path = xml_path
        self.xsd_path = xsd_path

    def extract_xml_from_rec_file(self):
        """ Extract XML from REC file """

        with open(self.rec_path, 'rb') as rec_file:
            with open(self.xml_path, 'w+') as xml_file:
                binary = '</Configuration>\n'.encode()
                for line in rec_file:
                    xml_file.write(line.decode())
                    if line.find(binary) != -1:
                        break

    def read_xml_from_rec_file(self):
        """ Read XML from REC file """

        with open(self.rec_path, 'rb') as rec_file:
            binary = '</Configuration>\n'.encode()
            for line in rec_file:
                logging.info(line)
                if line.find(binary) != -1:
                    break

    def read_xml_from_xml_file(self):
        """ Read XML through logging.info """

        with open(self.xml_path, 'rb') as xml_file:
            for line in xml_file:
                logging.info(line)

    def set_rec_path(self, rec_path):
        """ Set path to REC file """

        self.rec_path = rec_path

    def set_xml_path(self, xml_path):
        """ Set path to XML file """

        self.xml_path = xml_path

    def get_rec_path(self):
        """ Get path to REC file """

        return self.rec_path

    def get_xml_path(self):
        """ Get path to XML file """

        return self.xml_path

    def is_valid(self):
        """ Check if XML is valid with XSD file """
        if self.xsd_path is not None:
            xsd_file = XMLSchema(self.xsd_path)
            xml_file = ElementTree.parse(self.get_xml_path())
            return xsd_file.is_valid(xml_file)
        return False
