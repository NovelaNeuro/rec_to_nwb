import logging.config
import os  #

from mountainlab_pytools.mdaio import readmda

from src.datamigration.nwb_builder.managers.timestamps_manager_interface import TimestampManagerInterface

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaTimestampDataManager(TimestampManagerInterface):
    @staticmethod
    def __read_timestamps(directories, dataset_id):
        return readmda(directories[0][dataset_id])

    # override
    def read_data(self, dataset_id):
        timestamps = self.__read_timestamps(self.directories, dataset_id)
        continuous_time_dict = self.__get_continuous_time_dict(dataset_id)
        converted_timestamps = self.__convert_timestamps(continuous_time_dict, timestamps)

        return converted_timestamps

    # override
    def get_final_data_shape(self):
        return sum(self.file_lenghts_in_datasets),
