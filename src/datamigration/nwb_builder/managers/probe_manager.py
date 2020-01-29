class ProbeManager:

    @staticmethod
    def get_probe_file(probes, device_type):
        for probe_metadata in probes:
            if probe_metadata['probe_type'] == device_type:
                return probe_metadata