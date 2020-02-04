import yaml


class ProbesExtractor:

    def __init__(self):
        self.probes_content = []

    def extract_probes_metadata(self, probes_paths):
        for probe_file in probes_paths:
            with open(probe_file, 'r') as stream:
                self.probes_content.append(yaml.safe_load(stream))

    def get_probe_file(self, device_type):
        #ToDo  Maybe we can use dict k = probe_Type v = probe file
        for probe_metadata in self.probes_content:
            if probe_metadata['probe_type'] == device_type:
                return probe_metadata
        return None
