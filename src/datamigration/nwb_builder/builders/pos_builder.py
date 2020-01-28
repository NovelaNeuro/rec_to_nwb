from src.datamigration.nwb_builder.extractors.pos_extractor import POSExtractor


def build_position(datasets, nwb_content):
    pos_extractor = POSExtractor(datasets)
    nwb_content.processing["behavior"].add_data_interface(pos_extractor.get_position())
