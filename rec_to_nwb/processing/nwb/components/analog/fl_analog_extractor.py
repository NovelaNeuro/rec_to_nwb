import logging.config
import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from rec_to_nwb.processing.time.continuous_time_extractor import ContinuousTimeExtractor
from rec_to_nwb.processing.time.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class FlAnalogExtractor:

    @staticmethod
    def extract_analog_for_single_dataset(analog_files, continuous_time_file,
                                        convert_timestamps=True):
        single_dataset_data = {}
        for analog_sensor in analog_files:
            analog_data = readTrodesExtractedDataFile(analog_files[analog_sensor])
            if not 'timestamps' in analog_sensor:
                values = analog_data['data']
                single_dataset_data[analog_data['id']] = values
            else:
                timestamps = FlAnalogExtractor._extract_analog_timestamps(
                        analog_data, continuous_time_file, convert_timestamps)
                single_dataset_data[analog_sensor] = timestamps
        return single_dataset_data

    @staticmethod
    def _extract_analog_timestamps(analog_data, continuous_time_file, convert_timestamps):
        timestamps = analog_data['data']['time']
        if convert_timestamps:
            continuous_time = ContinuousTimeExtractor.get_continuous_time_array_file(continuous_time_file)
            return TimestampConverter.convert_timestamps(continuous_time, timestamps)
        else:
            # for old dataset, skip real-time conversion and just report Trodes time counts,
            # because the adjusted_systime is not ready
            return timestamps
