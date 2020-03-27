

class PreprocessingValidator():
    def __init__(self, all_data_dirs, epochs, data_types_to_check):
        self.all_data_dirs = all_data_dirs
        self.epochs = epochs
        self.data_types_to_check = data_types_to_check
        self.dicts = self.__create_existing_data_dictionary()


    def return_missing_preprocessing_data(self):
        """returns string with missing preprocessing files"""
        for epoch in self.epochs:
            self.__check_single_epoch(epoch)
        return self.__log_missing_files()

    def __log_missing_files(self):
        """converts dictionary with missing files to string"""
        missing_data_types = ''
        for epoch in self.epochs:
            for data_type in self.dicts[epoch]:
                if self.dicts[epoch][data_type] == False:
                    missing_data_types += data_type + " files in epoch " + epoch + '\n'
        return missing_data_types

    def __check_single_epoch(self, epoch):
        """finds missing data in single epoch"""
        for data_type in self.dicts[epoch]:
            for data_dirs in self.all_data_dirs:
                if data_dirs.endswith(data_type) and epoch in data_dirs:
                    self.dicts[epoch][data_type] = True

    def __create_existing_data_dictionary(self):
        """create dictionary of preprocessing data for all epochs"""
        data_dictionary = {}
        for epoch in self.epochs:
            data_dictionary[epoch] = {}
            for data_type in self.data_types_to_check:
                data_dictionary[epoch][data_type] = False
        return data_dictionary
