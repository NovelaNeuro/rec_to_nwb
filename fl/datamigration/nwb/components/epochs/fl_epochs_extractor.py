from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class FlEpochsExtractor:


    @staticmethod
    def extract_epochs(continuous_time_files):
        session_start_times = []
        session_end_times = []
        for continuous_time_file in continuous_time_files:
            continuous_time_data = FlEpochsExtractor.__read_contunious_time_file(continuous_time_file)
            session_start_times.append(float(continuous_time_data['data'][0][1]))
            session_end_times.append(float(continuous_time_data['data'][-1][1]))
        return session_start_times, session_end_times

    @staticmethod
    def __read_contunious_time_file(continuous_time_file):
        return readTrodesExtractedDataFile(continuous_time_file)
