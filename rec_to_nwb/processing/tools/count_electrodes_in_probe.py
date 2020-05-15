from rec_to_nwb.processing.tools.beartype.beartype import beartype


@beartype
def count_electrodes_in_probe(probe_content: dict) -> int:
    return sum([
        len(shank['electrodes'])
        for shank in probe_content['shanks']
    ])
