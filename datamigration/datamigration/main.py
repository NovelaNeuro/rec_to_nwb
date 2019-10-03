import logging
import pathlib
import xml.etree.ElementTree as et


class XMLParser:
    file_path = ''

    def __init__(self, file_path='../data/fl_lab_header.xml'):
        self.file_path = file_path
        if pathlib.Path(self.file_path).exists():
            self.file_xml = open(file_path, 'r')

    def get_tree(self):
        tree = et.parse(self.file_xml)
        return tree

    def get_root(self):
        return self.get_tree().getroot()

    def get_element(self, name):
        path = "./" + name
        return self.get_root().find(path)

    def get_elements(self, name):
        path = "./" + name + '/'
        return [i for i in self.get_root().findall(path)]

    def get_internal_elements(self, name):
        path = "./" + name
        return find(path).getchildren()

    def get_element_specification(self, name):
        return [element for element in self.get_tree().iter(tag=name)]

    #def show_all(self, ):
    #    children = self.get_root().getchildren()
    #    for child in children:
    #        et.dump(child)


if __name__ == '__main__':
    xml_parser = XMLParser()
