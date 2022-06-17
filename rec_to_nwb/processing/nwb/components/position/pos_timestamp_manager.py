import logging.config
import os

import numpy as np
import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile
from rec_to_nwb.processing.nwb.common.timestamps_manager import \
    TimestampManager

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(
    fname=os.path.join(str(path), os.pardir, os.pardir,
                       os.pardir, os.pardir, 'logging.conf'),
    disable_existing_loggers=False)
logger = logging.getLogger(__name__)


NANOSECONDS_PER_SECOND = 1E9


class PosTimestampManager(TimestampManager):
    def __init__(self, directories, continuous_time_directories,
                 convert_timestamps=True):
        TimestampManager.__init__(
            self, directories, continuous_time_directories)
        self.convert_timestamps = convert_timestamps

    # override
    def _get_timestamps(self, dataset_id):
        """Gets timestamps from the online position tracking"""
        pos_online = readTrodesExtractedDataFile(
            self.directories[dataset_id][0])
        position = pd.DataFrame(pos_online['data'])
        return position.time.unique().astype('int64')

    def retrieve_real_timestamps(self, dataset_id):
        """Gets the corresponding Trodes timestamps from the online position
        tracking and matches them to the PTP time in the video file.

        Otherwise, we get the corresponding timestamps from
        continuous time which corresponds to the neural recording time stamps.

        If there is no corresponding timestamp, the result will be NaN.

        Parameters
        ----------
        dataset_id : int
            Index of the epoch

        Returns
        -------
        timestamps : ndarray, shape (n_online_tracked_positions,)

        """
        try:
            # Get online position tracking data
            pos_online_path = self.directories[dataset_id][0]
            pos_online = readTrodesExtractedDataFile(pos_online_path)
            pos_online = pd.DataFrame(pos_online['data'])
            # Make sure to get only the unique timestamps because they can
            # sometimes repeat after a jump in timestamps
            online_timestamps_ind = pos_online.time.unique().astype(np.uint64)

            # Get video PTP timestamps
            camera_hwsync = readTrodesExtractedDataFile(
                pos_online_path.replace(
                    '.pos_online.dat', '.pos_cameraHWFrameCount.dat'))
            camera_hwsync = (pd.DataFrame(camera_hwsync['data'])
                             .set_index('PosTimestamp'))

            # Find the PTP timestamps that correspond to position tracking
            # Convert from nanoseconds to seconds
            return (camera_hwsync.loc[online_timestamps_ind, 'HWTimestamp']
                    / NANOSECONDS_PER_SECOND).to_numpy()
        except KeyError:
            # If PTP timestamps do not exist find the corresponding timestamps
            # from the neural recording
            logger.info('No PTP timestamps found. Using neural timestamps.')
            return TimestampManager.retrieve_real_timestamps(
                self, dataset_id,
                convert_timestamps=self.convert_timestamps)
