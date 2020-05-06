def filter_probe_by_type(probes_content, device_type):
    for probe_metadata in probes_content:
        if probe_metadata['probe_type'] == device_type:
            return probe_metadata
    return None
