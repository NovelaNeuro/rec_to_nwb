import logging.config
import os

from pynwb import ProcessingModule

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ProcessingModuleCreator:

    def __init__(self, name, description):
        self.processing_module = ProcessingModule(name, description)

    def insert(self, data):
        try:
            self.processing_module.add(data)
        except TypeError as err:
            # log error instead
            logger.error('Inserting data into time module has failed: ' + str(err))
