import xml.etree.ElementTree as ET


class XmlHeaderView:

    def __init__(self, filename):
        self.tree = ET.parse(filename)

    def getRoot(self):
        return self.tree.getroot()
