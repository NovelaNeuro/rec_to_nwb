import logging.config
import os

from rec_to_nwb.processing.validation.associated_files_validation_summary import \
    AssociatedFilesValidationSummary
from rec_to_nwb.processing.validation.validator import Validator

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=os.path.join(str(path), os.pardir, os.pardir, 'logging.conf'),
    disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class AssociatedFilesValidator(Validator):

    def __init__(self, associated_files):
        self.associated_files = associated_files

    def create_summary(self):
        if len(self.associated_files) == 0:
            logger.info(
                "There are no associated_files defined in metadata.yml file.")
        return AssociatedFilesValidationSummary(self.associated_files)
