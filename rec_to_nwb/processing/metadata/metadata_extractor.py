import json

import yaml


class MetadataExtractor:
    @staticmethod
    def extract_metadata(metadata_path):
        with open(metadata_path, "r") as stream:
            yaml_dict = yaml.safe_load(stream)

            try:
                # yaml automatically converts date_of_birth to a datetime object, need to convert back
                yaml_dict["subject"]["date_of_birth"] = yaml_dict["subject"][
                    "date_of_birth"
                ].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            except KeyError:
                pass
            # for some reason they want to convert all ints, float to strings
            return json.loads(json.dumps(yaml_dict), parse_int=str, parse_float=str)
