import logging.config
import os

from rec_to_nwb.processing.nwb.components.processing_module.processing_module_creator import \
    ProcessingModuleCreator

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ProcessingModuleOriginator:

    @staticmethod
    def make(nwb_content):
        logger.info('ProcessingModule: Creating behavior')
        pm_creator = ProcessingModuleCreator(
            'behavior', 'Contains all behavior-related data')
        logger.info('ProcessingModule: Injecting behavior')
        nwb_content.add_processing_module(pm_creator.processing_module)

        logger.info('ProcessingModule: Creating tasks')
        pm_creator = ProcessingModuleCreator(
            'tasks', 'Contains all tasks information')
        logger.info('ProcessingModule: Injecting tasks')
        nwb_content.add_processing_module(pm_creator.processing_module)

        logger.info('ProcessingModule: Creating associated files')
        pm_creator = ProcessingModuleCreator(
            'associated_files', 'Contains all associated files data')
        logger.info('ProcessingModule: Injecting associated files')
        nwb_content.add_processing_module(pm_creator.processing_module)

        logger.info('ProcessingModule: Creating video files')
        pm_creator = ProcessingModuleCreator(
            'video_files', 'Contains all associated video files data')
        logger.info('ProcessingModule: Injecting video files')
        nwb_content.add_processing_module(pm_creator.processing_module)

        logger.info('ProcessingModule: Creating analog')
        pm_creator = ProcessingModuleCreator(
            'analog', 'Contains all analog data')
        logger.info('ProcessingModule: Injecting analog')
        nwb_content.add_processing_module(pm_creator.processing_module)

        logger.info(
            'ProcessingModule: Creating sample count-timestamp corespondence')
        pm_creator = ProcessingModuleCreator(
            'sample_count', 'corespondence between sample count and timestamps')
        logger.info(
            'ProcessingModule: Injecting sample count-timestamp corespondence')
        nwb_content.add_processing_module(pm_creator.processing_module)

        logger.info('ProcessingModule: Creating Camera Sample Frame Counts')
        pm_creator = ProcessingModuleCreator(
            'camera_sample_frame_counts', 'Camera Sample Frame Counts')
        logger.info('ProcessingModule: Injecting camera_sample_frame_counts')
        nwb_content.add_processing_module(pm_creator.processing_module)
