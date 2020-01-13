import yaml


class ProbesExtractor:

    def __init__(self, probes_paths):
        self.probes_content = []
        for probe_file in probes_paths:
            with open(probe_file, 'r') as stream:
                self.probes_content.append(yaml.safe_load(stream))
