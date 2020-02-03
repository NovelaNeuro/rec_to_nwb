

import logging.config
import os

from pynwb import ecephys

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaCreator:

    @staticmethod
    def create_mda(sampling_rate, electrode_table_region, extracted_mda_data):
        return ecephys.ElectricalSeries(
            name="e-series",
            data=extracted_mda_data.mda_data,
            electrodes=electrode_table_region,
            timestamps=extracted_mda_data.mda_timestamps,
            resolution=sampling_rate,
            comments="sample comment",
            description="Electrical series registered on electrode"
        )
