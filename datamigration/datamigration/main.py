import logging
import pathlib
import xml.etree.ElementTree as et


class XMLParser:
    file_path = ''

    def __init__(self, file_path='../data/fl_lab_header.xml'):
        self.file_path = file_path

    def open_xml(self):
        if pathlib.Path(self.file_path).exists():
            with open(self.file_path, 'r') as f:
                tree = et.parse(f)
                return tree

    def get_root(self):
        configuration = self.open_xml().getroot()
        return configuration

    def get_element(self, name):
        path = "./" + name
        element = self.get_root().findall(path)
        return element

    def get_elements(self, name):
        path = "./" + name + '/'
        elements = []
        for i in self.get_root().findall(path):
            elements.append(i)
        return elements

    def get_element_specification(self, name):
        elements = []
        for element in self.open_xml().iter(tag=name):
            elements.append(element)
        return elements

    def show_all(self, ):
        children = self.get_root().getchildren()
        for child in children:
            et.dump(child)


if __name__ == '__main__':
    xml_parser = XMLParser()
    xml_parser.show_all()
