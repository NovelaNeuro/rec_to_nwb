import os

from fl.datamigration.exceptions.missing_data_exception import MissingDataException


class InputValidator:
    def validate_input_data(self, metadata_path, probes_paths, all_data_dirs, epochs, data_types_to_check):
        missing_data = self.return_missing_metadata(metadata_path, probes_paths)
        missing_data += self.return_missing_data(all_data_dirs, epochs, data_types_to_check)
        if not missing_data == '':
            raise MissingDataException(missing_data + "are missing")
        return missing_data

    def return_missing_metadata(self, metadata_path, probes_paths):
        missing_data = ''
        if not(os.path.exists(metadata_path)):
            missing_data += metadata_path + '\n'
        for probe_path in probes_paths:
            if not(os.path.exists(probe_path)):
                missing_data += probe_path + '\n'
        return missing_data

    def return_missing_data(self, all_data_dirs, epochs, data_types_to_check):
        dicts = self.__create_dicts(epochs, data_types_to_check)
        for epoch in epochs:
            self.__check_single_epoch(all_data_dirs, dicts, epoch)
        return self.__log_missing_files(epochs, dicts)

    def __log_missing_files(self, epochs, dicts):
        missing_data_types = ''
        for epoch in epochs:
            for data_type in dicts[epoch]:
                if dicts[epoch][data_type] == False:
                    missing_data_types += data_type + " files in epoch " + epoch + '\n'
        return missing_data_types

    @staticmethod
    def __check_single_epoch(all_data_dirs, dicts, epoch):
        for data_type in dicts[epoch]:
            for data_dirs in all_data_dirs:
                if data_dirs.endswith(data_type) and epoch in data_dirs:
                    dicts[epoch][data_type] = True

    @staticmethod
    def __create_dicts(epochs, data_types_to_check):
        new_dict = {}
        for epoch in epochs:
            new_dict[epoch] = {}
            for data_type in data_types_to_check:
                new_dict[epoch][data_type] = False
        return new_dict
