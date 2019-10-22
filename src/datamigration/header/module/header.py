import xml.etree.ElementTree as ET

from .configuration import Configuration


class Header:

    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.configuration = Configuration(self.tree.getroot())
