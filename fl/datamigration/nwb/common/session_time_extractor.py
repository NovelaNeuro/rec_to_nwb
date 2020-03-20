from datetime import datetime

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class SessionTimeExtractor:

    def __init__(self, datasets, animal_name, date, dataset_names):
        self.datasets = datasets
        self.animal_name = animal_name
        self.date = date
        self.dataset_names = dataset_names

    def get_session_start_time(self):
        continuous_time_file = \
            self.datasets[0].data['time'] + '/' + self.date + '_' + self.animal_name + '_' \
            + self.dataset_names[0] + '.continuoustime.dat'
        continuous_time = SessionTimeExtractor.__read_continuous_time(continuous_time_file)
        session_start_timestamp = continuous_time['system_time_at_creation']
        session_start_datetime = datetime.fromtimestamp(int(session_start_timestamp)/1E3)
        return session_start_datetime

    @staticmethod
    def __read_continuous_time(continuous_time_file):
        return readTrodesExtractedDataFile(continuous_time_file)
