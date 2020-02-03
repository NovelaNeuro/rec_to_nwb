import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NTrodesInjector:
    @staticmethod
    def inject_ntrode(nwb_content, ntrode):
        nwb_content.add_electrode_group(ntrode)
