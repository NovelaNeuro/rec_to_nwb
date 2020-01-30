from src.datamigration.extension.ntrode import NTrode


def build_ntrodes(metadata, nwb_content):
    fl_ntrodes = []
    for ntrode_metadata in metadata['ntrode probe channel map']:
        fl_ntrode = create_ntrode(ntrode_metadata, nwb_content.devices)
        fl_ntrodes.append(fl_ntrode)
    for fl_ntrode in fl_ntrodes:
        nwb_content.add_electrode_group(fl_ntrode)


def create_ntrode(metadata, devices):
    probe_id = str(metadata["probe_id"])
    device = devices[probe_id]

    map_list = []
    for map_element in metadata['map'].keys():
        map_list.append((map_element, metadata['map'][map_element]))

    ntrode = NTrode(
        probe_id=metadata["probe_id"],
        ntrode_id=metadata['ntrode_id'],
        device=device,
        location='-',
        description='-',
        name='ntrode ' + str(metadata['ntrode_id']),
        map=map_list
    )
    return ntrode
