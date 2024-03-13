from rec_to_nwb.processing.exceptions.invalid_metadata_exception import \
    InvalidMetadataException


def filter_probe_by_type(probes_content, device_type):
    for probe_metadata in probes_content:
        if probe_metadata['probe_type'] == device_type:
            return probe_metadata
    if device_type not in [probe_metadata['probe_type'] for probe_metadata in probes_content]:
        raise InvalidMetadataException(
            'there is not matching device type for metadata electrode_group in probe.yml schemas: ' + str(device_type))
    return None
