import xml.etree.ElementTree as ET


class XmlHeaderView:

    def __init__(self, filename):
        self.tree = ET.parse(filename)

    def get_Configuration(self):
        return self.tree.getroot()

    def get_GlobalConfiguration(self):
        return self.tree.find('GlobalConfiguration')

    def get_HardwareConfiguration(self):
        return self.tree.find('HardwareConfiguration')

    def get_Devices(self):
        return self.tree.findall('.//Device')

    def get_Channels(self):
        return self.tree.findall('.//Channel')
