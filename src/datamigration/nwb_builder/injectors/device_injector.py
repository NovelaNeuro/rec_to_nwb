import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DeviceInjector():
    def __init__(self, nwb_content):
        self.nwb_content = nwb_content


    def join_device(self, device):
        self.nwb_content.add_device(device)