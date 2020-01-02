import fnmatch
import os

import yaml


class ProbesExtractor:

    def __init__(self, probes_path):
        # self.probe = Probe(probe_folder_path)

        for probe_file in os.listdir(probes_path):
            if fnmatch.fnmatch(probe_file, "probe*.yml"):
                with open(probes_path + probe_file, 'r') as stream:
                    self.probe_content = yaml.safe_load(stream)
                    print(self.probe_content)
                    # self.electrodes = [Electrode(electrode) for electrode in self.probe_content['shanks']]

        self.probes = {}
