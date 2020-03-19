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
        continuous_time = readTrodesExtractedDataFile(continuous_time_file)
        session_start_timestamp = continuous_time['data'][0][1]
        session_start_datetime = datetime.fromtimestamp(session_start_timestamp / 1E9)
        return session_start_datetime
