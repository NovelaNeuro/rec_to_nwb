import os
import logging.config

from rec_to_nwb.processing.nwb.components.mda.electrical_series_creator import ElectricalSeriesCreator
from rec_to_nwb.processing.nwb.components.mda.fl_mda_manager import FlMdaManager
from rec_to_nwb.processing.nwb.components.mda.mda_injector import MdaInjector
from rec_to_nwb.processing.nwb.components.mda.old_fl_mda_manager import OldFlMdaManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class OldMdaOriginator:
    def __init__(self, datasets, header, metadata):
        self.datasets = datasets
        self.header = header
        self.metadata = metadata

    def make(self, nwb_content):
        logger.info('MDA: Building')
        old_fl_mda_manager = OldFlMdaManager(
            nwb_content=nwb_content,
            sampling_rate=float(self.header.configuration.hardware_configuration.sampling_rate),
            datasets=self.datasets,
            conversion=self.metadata['raw_data_to_volts']
        )
        fl_mda = old_fl_mda_manager.get_data()
        logger.info('MDA: Injecting')
        MdaInjector.inject_mda(
            nwb_content=nwb_content,
            electrical_series=ElectricalSeriesCreator.create_mda(fl_mda)
        )