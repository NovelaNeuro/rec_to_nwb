
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_manager import FlInvalidTimeManager
from fl.datamigration.nwb.components.invalid_times.fl_invalid_time_pos_timestamp_extractor import \
    FlInvalidTimePosTimestampExtractor


class FlPosInvalidTimeManager(FlInvalidTimeManager):
    def __init__(self, datasets):
        FlInvalidTimeManager.__init__(self, datasets)
        self.pos_timestamps_extractor = FlInvalidTimePosTimestampExtractor(datasets)

    def build_pos_invalid_times(self):
        timestamps = self.pos_timestamps_extractor.get_converted_timestamps()
        return self.build(timestamps, 'pos', self.__calculate_pos_period(timestamps))

    def __calculate_pos_period(self, timestamps):
        number_of_invalid_records_at_start_of_a_file = 0
        number_of_invalid_records_at_end_of_a_file = 0
        first_timestamp = timestamps[0][0]
        last_timestamp = timestamps[-1][-1]
        len_of_timestamps = 0
        for single_epoch_timestamps in timestamps:
            len_of_timestamps += len(single_epoch_timestamps)
        while not first_timestamp >= 0:
            number_of_invalid_records_at_start_of_a_file += 1
            first_timestamp = timestamps[0][number_of_invalid_records_at_start_of_a_file]
        while not last_timestamp >= 0:
            number_of_invalid_records_at_end_of_a_file += 1
            last_timestamp = timestamps[-1][(-1 - number_of_invalid_records_at_end_of_a_file)]
        return (last_timestamp - first_timestamp) / \
               (len_of_timestamps - number_of_invalid_records_at_end_of_a_file -
                number_of_invalid_records_at_start_of_a_file)