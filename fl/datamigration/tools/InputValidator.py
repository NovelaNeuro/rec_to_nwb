import os

from fl.datamigration.exceptions.missing_data_exception import MissingDataException


class InputValidator:
    def __init__(self, data_types_to_check):
        self.data_types_to_check = data_types_to_check

    def validate_metadata_exists(self, metadata_path, probes_paths):
        if not(os.path.exists(metadata_path)):
            raise MissingDataException(str(metadata_path + " is missing"))
        for probe_path in probes_paths:
            if not(os.path.exists(probe_path)):
                raise MissingDataException(str(probe_path) + " is missing")

    def validate_datasets_exist(self, data_path, animal, date, epochs):
        all_data_dirs = self.__get_all_data_directories(data_path, animal, date)
        dicts = self.__create_dicts(epochs, self.data_types_to_check)
        for epoch in epochs:
            self.__check_single_epoch(all_data_dirs, dicts, epoch)
        self.__log_missing_files(epochs, dicts)
        return dicts

    def __log_missing_files(self, epochs, dicts):
        missing_data_types = ''
        for epoch in epochs:
            for data_type in dicts[epoch]:
                if dicts[epoch][data_type] == False:
                    missing_data_types += data_type + " "
        print(missing_data_types)
        if missing_data_types != '':
            raise MissingDataException(missing_data_types + "are missing from epoch " + epoch)

    @staticmethod
    def __check_single_epoch(all_data_dirs, dicts, epoch):
        for data_type in dicts[epoch]:
            for data_dirs in all_data_dirs:
                if data_dirs.endswith(data_type) and epoch in data_dirs:
                    dicts[epoch][data_type] = True

    @staticmethod
    def __get_all_data_directories(data_path, animal, date):
        if not(os.path.exists(data_path + '/' + animal + '/preprocessing/' + date)):
            raise MissingDataException('missing ' + data_path + ' directory')
        return os.listdir(data_path + '/' + animal + '/preprocessing/' + date)

    @staticmethod
    def __create_dicts(epochs, data_types_to_check):
        new_dict = {}
        for epoch in epochs:
            new_dict[epoch] = {}
            for data_type in data_types_to_check:
                new_dict[epoch][data_type] = False
        return new_dict
