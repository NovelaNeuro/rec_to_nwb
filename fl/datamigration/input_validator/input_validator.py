import os

from fl.datamigration.exceptions.missing_data_exception import MissingDataException
from fl.datamigration.input_validator.metadata_validator import MetadataValidator
from fl.datamigration.input_validator.preprocessing_validator import PreprocessingValidator


class InputValidator:
    """ Class to validate if input data is complete

        Methods:
            validate_input_data()
            return_missing_metadata()
            return_missing_preprocessing_data()
            __log_missing_files()
            __check_single_epoch()
            __create_existing_data_dictionary()
        """
    def __init__(self, metadata_path, probes_paths, all_data_dirs, epochs, data_types_to_check):
        self.metadata_validator = MetadataValidator(metadata_path, probes_paths)
        self.preprocessing_validator = PreprocessingValidator(all_data_dirs, epochs, data_types_to_check)

    def validate_input_data(self, metadata_path, probes_paths, all_data_dirs, epochs, data_types_to_check):
        """Raises exception if data is incomplete"""
        missing_metadata = self.metadata_validator.get_missing_metadata()
        missing_preprocessing_data = self.preprocessing_validator.get_missing_preprocessing_data()

        if not missing_data == '':
            raise MissingDataException(missing_data + "are missing")
        return missing_data
