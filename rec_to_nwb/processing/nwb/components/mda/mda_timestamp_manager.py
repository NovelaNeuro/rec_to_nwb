import logging.config
import os

from mountainlab_pytools.mdaio import readmda
from rec_to_nwb.processing.nwb.common.timestamps_manager import \
    TimestampManager

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(
    fname=os.path.join(str(path), os.pardir, os.pardir,
                       os.pardir, os.pardir, 'logging.conf'),
    disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaTimestampDataManager(TimestampManager):
    def __init__(self, directories, continuous_time_directories):
        TimestampManager.__init__(
            self, directories, continuous_time_directories)

    def _get_timestamps(self, dataset_id):
        return readmda(self.directories[dataset_id][0])
