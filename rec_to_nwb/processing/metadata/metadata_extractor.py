import json

import yaml


class MetadataExtractor:

    @staticmethod
    def extract_metadata(metadata_path):
        with open(metadata_path, 'r') as stream:
            return json.loads(
                json.dumps(yaml.safe_load(stream)),
                parse_int=str,
                parse_float=str)
