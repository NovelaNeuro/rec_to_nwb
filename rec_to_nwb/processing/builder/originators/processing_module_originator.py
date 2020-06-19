import logging.config
import os

from rec_to_nwb.processing.nwb.components.processing_module.processing_module_creator import ProcessingModuleCreator

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ProcessingModuleOriginator:

    @staticmethod
    def make(nwb_content):
        logger.info('ProcessingModule: Creating')
        pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')
        logger.info('ProcessingModule: Injecting')
        nwb_content.add_processing_module(pm_creator.processing_module)
