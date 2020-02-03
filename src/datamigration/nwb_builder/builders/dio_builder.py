import logging.config
import os

from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioBuilder:
    def __init__(self, metadata, data_path):
        self.metadata = metadata
        self.data_path = data_path

    def build(self):
        return DioExtractor(
            data_path=self.data_path,
            metadata=self.metadata
        ).get_dio()
