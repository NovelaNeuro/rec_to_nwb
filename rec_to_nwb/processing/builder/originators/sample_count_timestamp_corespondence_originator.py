import logging.config
import os

from rec_to_nwb.processing.nwb.components.sample_count_timestamp_corespondence.sample_count_timestamp_corespondence_injector import \
    SampleCountTimestampCorespondenceInjector
from rec_to_nwb.processing.nwb.components.sample_count_timestamp_corespondence.sample_count_timestamp_corespondence_manager import \
    SampleCountTimestampCorespondenceManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=os.path.join(str(path), os.pardir, os.pardir,
                       os.pardir, 'logging.conf'),
    disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class SampleCountTimestampCorespondenceOriginator:
    def __init__(self, datasets):
        self.datasets = datasets

    def make(self, nwb_content):
        logger.info('Sample Count Timestamp Corespondence: Building')
        manager = SampleCountTimestampCorespondenceManager(
            datasets=self.datasets
        )
        timeseries = manager.get_timeseries()
        logger.info('Sample Count Timestamp Corespondence: Injecting')
        SampleCountTimestampCorespondenceInjector.inject(
            nwb_content=nwb_content,
            processing_module_name="sample_count",
            timeseries=timeseries
        )
