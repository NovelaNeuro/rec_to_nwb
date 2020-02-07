import yaml


class ProbesExtractor:

    def extract_probes_metadata(self, probes_paths):
        probes_content = []
        for probe_file in probes_paths:
            with open(probe_file, 'r') as stream:
                probes_content.append(yaml.safe_load(stream))
        return probes_content


