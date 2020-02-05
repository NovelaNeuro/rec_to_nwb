import yaml


class ProbesExtractor:

    def extract_probes_metadata(self, probes_paths):
        probes_content = []
        for probe_file in probes_paths:
            with open(probe_file, 'r') as stream:
                probes_content.append(yaml.safe_load(stream))
        return probes_content

    def get_probe_file(self, probes_content, device_type):
        #ToDo  Maybe we can use dict k = probe_Type v = probe file
        for probe_metadata in probes_content:
            if probe_metadata['probe_type'] == device_type:
                return probe_metadata
        return None
