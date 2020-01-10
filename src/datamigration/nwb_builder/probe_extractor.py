import fnmatch
import os

import yaml


class ProbesExtractor:

    def __init__(self, probes_path):
        self.probes_content = []
        for probe_file in os.listdir(probes_path):
            if fnmatch.fnmatch(probe_file, "probe*.yml"):
                with open(probes_path + probe_file, 'r') as stream:
                    self.probes_content.append(yaml.safe_load(stream))