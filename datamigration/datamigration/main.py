import logging
import pathlib
import xml.etree.ElementTree as et


def open_xml():
    file_path = '../data/fl_lab_header.xml'
    if pathlib.Path(file_path).exists():
        with open(file_path, 'r') as f:
            tree = et.parse(f)
            return tree


def get_root():
    configuration = open_xml().getroot()
    return configuration


def get_element(name):
    path = "./" + name
    element = get_root().findall(path)
    return element


def get_elements(name):
    path = "./" + name + '/'
    elements = []
    for i in get_root().findall(path):
        elements.append(i)
    return elements


def get_element_specification(name):
    elements = []
    for element in open_xml().iter(tag=name):
        elements.append(element)
    return elements


def show_all():
    children = get_root().getchildren()
    for child in children:
        et.dump(child)


if __name__ == '__main__':
    show_all()