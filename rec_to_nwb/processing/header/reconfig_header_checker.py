import os

import xmlschema

from rec_to_nwb.processing.validation.validation_registrator import ValidationRegistrator
from rec_to_nwb.processing.validation.xml_files_validation import XmlFilesValidator

path = os.path.dirname(os.path.abspath(__file__))


class ReconfigHeaderChecker:
    
    @classmethod
    def validate(cls, xml_header_path):
        if xml_header_path:
            cls.__validate_xml_header(xml_header_path)
            cls.__compare_with_xml_schema(xml_header_path)
            return xml_header_path
        else:
            return None

    @classmethod
    def __validate_xml_header(cls, xml_header_path):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(XmlFilesValidator(xml_header_path))
        validation_registrator.validate()

    @classmethod
    def __compare_with_xml_schema(cls, xml_header_path):
        xsd_file_path = str(path) + '/../../../rec_to_nwb/data/header_schema.xsd'
        xsd_schema = xmlschema.XMLSchema(xsd_file_path)
        xmlschema.validate(xml_header_path, xsd_schema)