def build_processing_module(name, description, nwb_content):
    nwb_content.create_processing_module(
        name=name,
        description=description
    )
