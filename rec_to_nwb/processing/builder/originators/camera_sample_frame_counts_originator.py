import logging.config
import os

from rec_to_nwb.processing.nwb.components.video_files.camera_sample_frame_counts.camera_sample_frame_counts_injector import \
    CameraSampleFrameCountsInjector
from rec_to_nwb.processing.nwb.components.video_files.camera_sample_frame_counts.camera_sample_frame_counts_manager import \
    CameraSampleFrameCountsManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=os.path.join(str(path), os.pardir, os.pardir,
                       os.pardir, 'logging.conf'),
    disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class CameraSampleFrameCountsOriginator:
    def __init__(self, raw_data_path):
        self.raw_data_path = raw_data_path

    def make(self, nwb_content):
        logger.info('Camera Sample Frame Counts Builder: Building')
        manager = CameraSampleFrameCountsManager(
            raw_data_path=self.raw_data_path
        )
        timeseries = manager.get_timeseries()
        logger.info('Camera Sample Frame Counts Builder: Injecting')
        CameraSampleFrameCountsInjector.inject(
            nwb_content=nwb_content,
            processing_module_name="camera_sample_frame_counts",
            timeseries=timeseries
        )
