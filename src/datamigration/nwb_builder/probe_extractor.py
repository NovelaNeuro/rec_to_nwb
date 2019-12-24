import yaml


class ProbeExtractor:

    def __init__(self, probe_path):
        with open(probe_path, 'r') as stream:
            print(yaml.safe_load(stream))


a = ProbeExtractor('probe3.yml')