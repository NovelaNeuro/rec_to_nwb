from rec_to_nwb.processing.nwb.components.video_files.camera_sample_frame_counts.camera_sample_frame_counts_builder import \
    CameraSampleFrameCountsBuilder
from rec_to_nwb.processing.nwb.components.video_files.camera_sample_frame_counts.camera_sample_frame_counts_extractor import \
    CameraSampleFrameCountsExtractor


class SampleCountTimestampCorespondenceManager:
    def __init__(self, datasets):
        self.continuous_time_files = [dataset.get_continuous_time() for dataset in datasets]
        self.extractor = CameraSampleFrameCountsExtractor(self.continuous_time_files)

    def get_timeseries(self):
        data = self.extractor.extract()
        builder = CameraSampleFrameCountsBuilder(data)
        return builder.build()