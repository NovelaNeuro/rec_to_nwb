import pandas  as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_manager import FlInvalidTimeManager


class FlPosFlInvalidTimeManager(FlInvalidTimeManager):
    def __init__(self, sampling_rate, datasets):
        FlInvalidTimeManager.__init__(self, sampling_rate, datasets)
        self.pos_timestamp_files = self.__get_pos_files()

    def build_pos_invalid_times(self):
        continuous_time_dicts = self._get_continuous_time_dicts()
        pos_timestamps = self.__read_pos_timestamps(self.__get_pos_files())
        return self.build(self._convert_timestamps(pos_timestamps, continuous_time_dicts), 'pos')

    def __get_pos_files(self):
        all_files = []
        for dataset in self.datasets:
            single_dataset_files = dataset.get_all_data_from_dataset('pos')
            for file in single_dataset_files:
                if file.endswith('pos_online.dat'):
                    all_files.append(dataset.get_data_path_from_dataset('pos') + file)
        return all_files

    def __read_pos_timestamps(self, timestamp_files):
        return [self.__read_single_pos_timestamps(timestamp_file) for timestamp_file in timestamp_files]

    def __read_single_pos_timestamps(self, timestamp_file):
        pos_online = readTrodesExtractedDataFile(timestamp_file)
        position = pd.DataFrame(pos_online['data'])
        return position.time.to_numpy(dtype='int64')

    def __calculate_pos_campling_rate(self):
        self.pos