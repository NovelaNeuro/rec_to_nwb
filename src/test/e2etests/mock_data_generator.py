import os


class Generator:
    def __init__(self, data_path):
        self.data_path = data_path
        self.extensions_table = ['pos', 'DIO', 'LFP', 'mda', 'metadata', 'mountain', 'spikes', 'time']
        self.pos_files = ['pos_cameraHWFrameCount.dat', 'pos_online.dat', 'pos_timestamps.dat']
        self.mda_files = ['exportmda.log', 'timestamps.mda']
        self.time_files = ['continuoustime.dat', 'exporttime.log', 'time.dat']
        self.DIO_files = ['exportdio.log']
        self.LFP_files = ['exportLFP.log', 'timestamps.dat']
        self.spike_files = ['exportspikes.log']

        # DIO, LFP, mda, spikes have multiple
        # mountain is empty
        # metadata has only metadata.yml
        self.files = dict([])
        self.files['pos'] = self.pos_files
        self.files['mda'] = self.mda_files
        self.files['time'] = self.time_files
        self.files['DIO'] = self.mda_files
        self.files['LFP'] = self.time_files
        self.files['metadata'] = []
        self.files['mountain'] = []
        self.files['spikes'] = self.spike_files

    def generate_new_data(self, animal_name, date, dataset):
        animal_path = self.data_path + '/' + animal_name
        date_path = animal_path + '/' + date
        if not os.path.exists(animal_path):
            os.mkdir(animal_path)
        if not os.path.exists(date_path):
            os.mkdir(date_path)
        if not os.path.exists(date_path + '/preprocessing'):
            os.mkdir(date_path + '/preprocessing')
        for extension in self.extensions_table:
            if not os.path.exists(date_path + '/preprocessing/' +
                                  self.generate_directory_name(animal_name, date, dataset, extension)):
                os.mkdir(date_path + '/preprocessing/' +
                         self.generate_directory_name(animal_name, date, dataset, extension))
            self.create_fake_files(date_path + '/preprocessing',
                                   extension,
                                   self.generate_directory_name(animal_name, date, dataset, ''))

            self.create_fake_mda(date_path + '/preprocessing',
                                 self.generate_directory_name(animal_name, date, dataset, ''))
            self.create_fake_DIO(date_path + '/preprocessing',
                                 self.generate_directory_name(animal_name, date, dataset, ''))
            self.create_fake_LFP(date_path + '/preprocessing',
                                 self.generate_directory_name(animal_name, date, dataset, ''))
            self.create_fake_spike(date_path + '/preprocessing',
                                   self.generate_directory_name(animal_name, date, dataset, ''))
            self.create_fake_metadata(date_path + '/preprocessing',
                                      self.generate_directory_name(animal_name, date, dataset, ''))

    def generate_directory_name(self, animal_name, date, dataset, extension):
        if not extension == 'pos':
            return date + '_' + animal_name + '_' + dataset + '.' + extension
        else:
            return date + '_' + animal_name + '_' + dataset + '.1.' + extension
            # requires some research if it is always 1

    def create_fake_files(self, path, extension, filename_front):
        for file in self.files[extension]:
            if extension == 'pos':
                if not os.path.exists(path + '/' + filename_front + '1.' + extension + '/' + filename_front + file):
                    open(path + '/' + filename_front + '1.' + extension + '/' + filename_front + file, 'a').close()
            else:
                if not os.path.exists(path + '/' + filename_front + extension + '/' + filename_front + file):
                    open(path + '/' + filename_front + extension + '/' + filename_front + file, 'a').close()

    def create_fake_mda(self, path, filename_front, count_of_mda_files=64):
        for i in range(count_of_mda_files):
            if not os.path.exists(path + '/' + filename_front + 'mda/' + filename_front + 'nt' + str(i + 1) + '.mda'):
                open(path + '/' + filename_front + 'mda/' + filename_front + 'nt' + str(i + 1) + '.mda', 'a').close()

    def create_fake_DIO(self, path, filename_front, count_of_DIO_files=32):
        for i in range(count_of_DIO_files):
            if not os.path.exists(
                    path + '/' + filename_front + 'DIO/' + filename_front + 'dio_Dout' + str(i + 1) + '.dat'):
                open(path + '/' + filename_front + 'DIO/' + filename_front + 'dio_Dout' + str(i + 1) + '.dat',
                     'a').close()
            if not os.path.exists(
                    path + '/' + filename_front + 'DIO/' + filename_front + 'dio_Din' + str(i + 1) + '.dat'):
                open(path + '/' + filename_front + 'DIO/' + filename_front + 'dio_Din' + str(i + 1) + '.dat',
                     'a').close()

    def create_fake_LFP(self, path, filename_front, count_of_LFP_files=64):
        for i in range(count_of_LFP_files):
            if not os.path.exists(
                    path + '/' + filename_front + 'LFP/' + filename_front + 'nt' + str(i + 1) + 'ch1.dat'):
                open(path + '/' + filename_front + 'LFP/' + filename_front + 'nt' + str(i + 1) + 'ch1.dat', 'a').close()

    def create_fake_spike(self, path, filename_front, count_of_spike_files=64):
        for i in range(count_of_spike_files):
            if not os.path.exists(
                    path + '/' + filename_front + 'spikes/' + filename_front + 'nt' + str(i + 1) + '.dat'):
                open(path + '/' + filename_front + 'spikes/' + filename_front + 'nt' + str(i + 1) + '.dat', 'a').close()

    def create_fake_metadata(self, path, filename_front):
        if not os.path.exists(path + '/' + filename_front + 'metadata/' + 'metadata.yml'):
            open(path + '/' + filename_front + 'metadata/' + 'metadata.yml', 'a').close()
