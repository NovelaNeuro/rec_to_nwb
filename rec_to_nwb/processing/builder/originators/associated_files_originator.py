import logging.config
import os

from rec_to_nwb.processing.nwb.components.associated_files.associated_files_creator import \
    AssociatedFilesCreator
from rec_to_nwb.processing.nwb.components.associated_files.associated_files_injector import \
    AssociatedFilesInjector
from rec_to_nwb.processing.nwb.components.associated_files.fl_associated_files_manager import \
    FlAssociatedFilesManager
from rec_to_nwb.processing.validation.associated_files_validation import \
    AssociatedFilesValidator
from rec_to_nwb.processing.validation.validation_registrator import \
    ValidationRegistrator

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=os.path.join(str(path), os.pardir, os.pardir,
                       os.pardir, 'logging.conf'),
    disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class AssociatedFilesOriginator:

    def __init__(self, metadata):
        if 'associated_files' in metadata:
            validation_registrator = ValidationRegistrator()
            validation_registrator.register(
                AssociatedFilesValidator(metadata['associated_files']))
            validation_registrator.validate()
            self.fl_associated_files_manager = FlAssociatedFilesManager(
                metadata['associated_files']
            )
            self.associated_files_creator = AssociatedFilesCreator()
            self.associated_files_injector = AssociatedFilesInjector()

    def make(self, nwb_content):
        logger.info('AssociatedFiles: Building')
        fl_associated_files = self.fl_associated_files_manager.get_fl_associated_files()
        logger.info('AssociatedFiles: Creating')
        associated_files = [
            self.associated_files_creator.create(fl_associated_file)
            for fl_associated_file in fl_associated_files
        ]
        logger.info('AssociatedFiles: Injecting')
        self.associated_files_injector.inject(
            associated_files, 'associated_files', nwb_content)
