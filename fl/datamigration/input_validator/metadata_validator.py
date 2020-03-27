import os


class MetadataValidator:
    def __init__(self, metadata_path, probes_paths):
        self.metadata_path = metadata_path
        self.probes_paths = probes_paths

    def return_missing_metadata(self):
        """returns string with all missing yml files"""
        missing_data = []
        if not (os.path.exists(self.metadata_path)):
            missing_data.append(self.metadata_path)
        for probe_path in self.probes_paths:
            if not (os.path.exists(probe_path)):
                missing_data.append(probe_path)
        return missing_data
