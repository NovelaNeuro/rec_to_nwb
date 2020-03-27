class PreprocessingValidator:
    """ Class to validate if preprocessing data is complete
        Args:
            all_data_dirs - all directories contained in directory <animal name>/<preprocessing>/<date>
            epochs - list of all epochs
            data_types_to_check - types of data required

        Methods:
            get_missing_preprocessing_data()
            __check_single_epoch()
        """

    def __init__(self, all_data_dirs, epochs, data_types_to_check):
        self.all_data_dirs = all_data_dirs
        self.epochs = epochs
        self.data_types_to_check = data_types_to_check

    def get_missing_preprocessing_data(self):
        """returns list of missing preprocessing files"""
        missing_data = []
        for epoch in self.epochs:
            missing_data.extend(self.__check_single_epoch(epoch))
        return missing_data

    def __check_single_epoch(self, epoch):
        """finds missing data in single epoch"""
        missing_data = []
        for data_type in self.data_types_to_check:
            is_data_present = False
            for data_dirs in self.all_data_dirs:
                if data_dirs.endswith(data_type) and epoch in data_dirs:
                    is_data_present = True
            if not is_data_present:
                missing_data.append((data_type, epoch))
        return missing_data
