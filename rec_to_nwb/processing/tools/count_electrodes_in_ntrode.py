from rec_to_nwb.processing.tools.beartype.beartype import beartype


@beartype
def count_electrodes_in_ntrode(ntrode_metadata: list, electrode_group_id) -> int:
    return sum([
        len(ntrode['map'])
        for ntrode in ntrode_metadata
        if ntrode['electrode_group_id'] == electrode_group_id
    ])
