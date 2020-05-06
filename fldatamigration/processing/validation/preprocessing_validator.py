import os

from fldatamigration.processing.exceptions.missing_data_exception import MissingDataException
from fldatamigration.processing.validation.preprocessing_validation_summary import PreprocessingValidationSummary
from fldatamigration.processing.validation.validator import Validator


class PreprocessingValidator(Validator):
    """ Class to validate if preprocessing data is complete

        Args:
            all_data_dirs (list of strings): all directories contained in directory <animal name>/<preprocessing>/<date>
            epochs (list of strings): list of all epochs
            data_types_to_check (dictionary): types of data required

        Methods:
            get_missing_preprocessing_data()
            __check_single_epoch()
        """

    def __init__(self, data_path, epochs, data_types_for_scanning):
        self.all_data_dirs = os.listdir(data_path)
        self.epochs = epochs
        self.data_types_for_scanning = data_types_for_scanning

    def create_summary(self):
        """Creates ValidationSummary object with the results of validation

            Returns:
                PreprocessingValidationSummary: missing preprocessing files
        """
        missing_preprocessing_data = self.__get_missing_preprocessing_data()
        message = ''
        if not missing_preprocessing_data == []:
            for missing_preprocessing_file in missing_preprocessing_data:
                message += missing_preprocessing_file[0] + ' from epoch ' + missing_preprocessing_file[1] + '\n'
            raise MissingDataException(message + "are missing")
        return PreprocessingValidationSummary(missing_preprocessing_data)

    def __get_missing_preprocessing_data(self):
        """Get list of missing preprocessing files

            Returns:
                List of strings: missing preprocessing files
        """
        missing_data = []
        for epoch in self.epochs:
            missing_data.extend(self.__check_single_epoch(epoch))
        return missing_data

    def __check_single_epoch(self, epoch):
        """finds missing data in single epoch

        Args:
            epoch (string): name of epoch to check

        Returns:
            List of strings: missing preprocessing files from checked epoch
        """
        missing_data = []
        for data_type in self.data_types_for_scanning:
            if self.data_types_for_scanning[data_type]:
                is_data_present = False
                for data_dirs in self.all_data_dirs:
                    if data_dirs.endswith(data_type) and epoch in data_dirs:
                        is_data_present = True
                if not is_data_present:
                    missing_data.append((data_type, epoch))
        return missing_data
