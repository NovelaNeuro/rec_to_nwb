import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodeGroupInjector:

    def __init__(self, nwb_content):
        self.nwb_content = nwb_content


    def join_electrode_group(self, electrode_group):
        self.nwb_content.add_electrode_group(electrode_group)