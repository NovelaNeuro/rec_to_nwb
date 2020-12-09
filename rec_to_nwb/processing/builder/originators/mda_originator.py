import os
import logging.config

from rec_to_nwb.processing.nwb.components.mda.electrical_series_creator import ElectricalSeriesCreator
from rec_to_nwb.processing.nwb.components.mda.fl_mda_manager import FlMdaManager
from rec_to_nwb.processing.nwb.components.mda.mda_injector import MdaInjector

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaOriginator:
    def __init__(self, datasets, header, metadata):
        self.datasets = datasets
        self.header = header
        self.metadata = metadata
        self.number_of_channels = self.count_number_of_channels(header)

    def make(self, nwb_content):
        logger.info('MDA: Building')
        fl_mda_manager = FlMdaManager(
            nwb_content=nwb_content,
            sampling_rate=float(self.header.configuration.hardware_configuration.sampling_rate),
            datasets=self.datasets,
            conversion=self.metadata['raw_data_to_volts'],
            number_of_channels=self.number_of_channels
        )
        fl_mda = fl_mda_manager.get_data()
        logger.info('MDA: Injecting')
        MdaInjector.inject_mda(
            nwb_content=nwb_content,
            electrical_series=ElectricalSeriesCreator.create_mda(fl_mda)
        )

    def count_number_of_channels(self, header):
        spike_configuration = header.configuration.spike_configuration
        counter = 0
        for spike_n_trode in spike_configuration.spike_n_trodes:
            counter += len(spike_n_trode.spike_channels)
        return counter