from rec_to_nwb.processing.nwb.components.video_files.fl_video_files_builder import FlVideoFilesBuilder
from rec_to_nwb.processing.nwb.components.video_files.fl_video_files_extractor import FlVideoFilesExtractor


class FlVideoFilesManager:

    def __init__(self, raw_data_path, video_directory, video_files_metadata):
        self.fl_video_files_extractor = FlVideoFilesExtractor(raw_data_path, video_directory, video_files_metadata)
        self.fl_video_files_builder = FlVideoFilesBuilder()

    def get_video_files(self):
        extracted_video_files = self.fl_video_files_extractor.extract_video_files()
        return [self.fl_video_files_builder.build(
            video_file["name"],
            video_file["timestamps"],
            video_file["devices"]
        ) for video_file in extracted_video_files]
