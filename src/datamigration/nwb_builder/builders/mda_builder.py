from datetime import datetime

from src.datamigration.nwb_builder.builders.table_region_builder import build_region
from src.datamigration.nwb_builder.extractors.mda_extractor import MdaExtractor


def build_mda(header, metadata, datasets, nwb_content):
    sampling_rate = header.configuration.hardware_configuration.sampling_rate
    experiment_start_time = datetime.strptime(
        metadata['session start time'], '%m/%d/%Y %H:%M:%S')
    mda_extractor = MdaExtractor(datasets, experiment_start_time)
    electrode_table_region = build_region(metadata, nwb_content)
    series = mda_extractor.get_mda(electrode_table_region, sampling_rate)
    nwb_content.add_acquisition(series)