def build_region(metadata, nwb_content):
    region = nwb_content.create_electrode_table_region(
        description=metadata['electrode region']['description'],
        region=metadata['electrode region']['region'],
        name='electrodes'
    )
    return region
