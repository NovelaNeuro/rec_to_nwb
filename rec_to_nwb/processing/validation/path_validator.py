import os

from rec_to_nwb.processing.validation.path_validation_summary import PathValidationSummary
from rec_to_nwb.processing.validation.validator import Validator


class PathValidator(Validator):
    def __init__(self, path):
        self.path = path

    def create_summary(self):
        if not os.path.isdir(self.path):
            raise NotADirectoryError(self.path + ' is not a directory')
        return PathValidationSummary()

