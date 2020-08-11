from rec_to_nwb.processing.nwb.components.sample_count_timestamp_corespondence.sample_count_timestamp_corespondence_extractor import \
    SampleCountTimestampCorespondenceExtractor
from rec_to_nwb.processing.nwb.components.sample_count_timestamp_corespondence.sample_count_timestamp_corespondence_builder import \
    SampleCountTimestampCorespondenceBuilder


class SampleCountTimestampCorespondenceManager:
    def __init__(self, datasets):
        self.continuous_time_files = [dataset.get_continuous_time() for dataset in datasets]
        self.extractor = SampleCountTimestampCorespondenceExtractor(self.continuous_time_files)

    def get_timeseries(self):
        data = self.extractor.extract()
        builder = SampleCountTimestampCorespondenceBuilder(data)
        return builder.build()
