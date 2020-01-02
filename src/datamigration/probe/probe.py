import yaml

from src.datamigration.probe.electrode import Electrode


class Probe:

    def __init__(self, probe_yml_path):
        with open(probe_yml_path, 'r') as stream:
            self.probe_content = yaml.safe_load(stream)
            self.electrodes = [Electrode(electrode) for electrode in self.probe_content['shanks']]

