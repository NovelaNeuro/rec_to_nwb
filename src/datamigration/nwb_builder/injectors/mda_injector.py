import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaInjector:

    @staticmethod
    def inject_mda(mda, nwb_content):
        nwb_content.add_acquisition(mda)
