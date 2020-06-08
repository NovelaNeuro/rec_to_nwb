import logging.config
import os

from rec_to_nwb.processing.nwb.components.epochs.epochs_injector import EpochsInjector
from rec_to_nwb.processing.nwb.components.epochs.fl_epochs_manager import FlEpochsManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class EpochsOriginator:

    def __init__(self, datasets):
        self.datasets = datasets

    def make(self, nwb_content):
        logger.info('Epochs: Building')
        fl_epochs_manager = FlEpochsManager(self.datasets)
        logger.info('Epochs: Creating')
        epochs = fl_epochs_manager.get_epochs()
        logger.info('Epochs: Injecting')
        EpochsInjector.inject(epochs, nwb_content)
