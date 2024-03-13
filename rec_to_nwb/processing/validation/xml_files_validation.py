import os

from rec_to_nwb.processing.exceptions.missing_data_exception import \
    MissingDataException
from rec_to_nwb.processing.validation.validation_registrator import \
    ValidationRegistrator
from rec_to_nwb.processing.validation.xml_files_validation_summary import \
    XmlFilesValidationSummary


class XmlFilesValidator(ValidationRegistrator):
    def __init__(self, path):
        self.path = path

    def create_summary(self):
        if not os.path.exists(self.path):
            raise MissingDataException(
                'xml file ' + self.path + ' does not exist!')
        return XmlFilesValidationSummary()
