import yaml


class MetadataExtractor:

    @staticmethod
    def extract_metadata(metadata_path):
        with open(metadata_path, 'r') as stream:
            return yaml.safe_load(stream)
