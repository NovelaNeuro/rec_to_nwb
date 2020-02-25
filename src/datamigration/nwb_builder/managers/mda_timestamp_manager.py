import logging.config
import os

from mountainlab_pytools.mdaio import readmda

from src.datamigration.nwb_builder.managers.timestamps_manager_interface import TimestampManagerInterface

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaTimestampDataManager(TimestampManagerInterface):
    def __init__(self, directories, continuous_time_directories):
        TimestampManagerInterface.__init__(self, directories, continuous_time_directories)

    def _get_timestamps(self, dataset_id):
        return readmda(self.directories[dataset_id])
    #
    # def read_data(self, dataset_id):
    #     timestamps = self._get_timestamps(dataset_id)
    #     continuous_time_dict = self.continuous_time_dicts[dataset_id]
    #     return self.timestamp_converter.convert_timestamps(continuous_time_dict, timestamps)
