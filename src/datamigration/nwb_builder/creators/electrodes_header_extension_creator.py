import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodesHeaderExtensionCreator:
    @staticmethod
    def create_electrodes_header_extension(header):
        hw_chan = []
        for spike_n_trode in header.configuration.spike_configuration.spike_n_trodes:
            for spike_channel in spike_n_trode.spike_channels:
                hw_chan.append(spike_channel.hw_chan)
        return hw_chan
