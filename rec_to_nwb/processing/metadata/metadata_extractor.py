import yaml
import json


class MetadataExtractor:

    @staticmethod
    def extract_metadata(metadata_path):
        with open(metadata_path, 'r') as stream:
            metadata_dict = yaml.safe_load(stream)
            metadata = json.loads(json.dumps(metadata_dict), parse_int=str, parse_float=str)
            return metadata
