import os

from fl.datamigration.exceptions.missing_data_exception import MissingDataException
from fl.datamigration.input_validator.metadata_validator import MetadataValidator
from fl.datamigration.input_validator.preprocessing_validator import PreprocessingValidator


class InputValidator:
    """ Class to validate if input data is complete
        Args:
            metadata_path - path to metadata.yml file
            probes_paths - list paths to yml files containing informations about probe types
            all_data_dirs - all directories contained in directory <animal name>/<preprocessing>/<date>
            epochs - list of all epochs
            data_types_to_check - types of data required

        Methods:
            validate_input_data()
        """
    def __init__(self, metadata_path, probes_paths, all_data_dirs, epochs, data_types_to_check):
        self.epochs = epochs
        self.metadata_validator = MetadataValidator(metadata_path, probes_paths)
        self.preprocessing_validator = PreprocessingValidator(all_data_dirs, epochs, data_types_to_check)

    def validate_input_data(self):
        """Raises exception if data is incomplete"""
        missing_metadata = self.metadata_validator.get_missing_metadata()
        missing_preprocessing_data = self.preprocessing_validator.get_missing_preprocessing_data()
        if not (missing_metadata == []) or not(missing_preprocessing_data == []):
            message = ''
            for missing_metadata_file in missing_metadata:
                message += missing_metadata_file + '\n'
            for missing_preprocessing_file in missing_preprocessing_data:
                message += missing_preprocessing_file[0] + ' from epoch ' + missing_preprocessing_file[1] + '\n'
            raise MissingDataException(message + "are missing")
