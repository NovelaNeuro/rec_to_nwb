import os


class MetadataValidator:
    """ Class to validate if metadata is complete
        Args:
            metadata_path (string): path to metadata.yml file
            probes_paths (list of strings): list paths to yml files containing informations about probe types

        Methods:
            get_missing_metadata()
        """

    def __init__(self, metadata_path, probes_paths):
        self.metadata_path = metadata_path
        self.probes_paths = probes_paths

    def get_missing_metadata(self):
        """Gets all missing yml files

        Returns:
            list of strings: list of all missing yml files
        """
        missing_data = []
        if not (os.path.exists(self.metadata_path)):
            missing_data.append(self.metadata_path)
        for probe_path in self.probes_paths:
            if not (os.path.exists(probe_path)):
                missing_data.append(probe_path)
        return missing_data
