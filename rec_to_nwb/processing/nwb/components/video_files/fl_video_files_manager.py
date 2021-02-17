from rec_to_nwb.processing.nwb.components.video_files.fl_video_files_builder import FlVideoFilesBuilder
from rec_to_nwb.processing.nwb.components.video_files.fl_video_files_extractor import FlVideoFilesExtractor
from rec_to_nwb.processing.nwb.components.video_files.video_files_copy_maker import VideoFilesCopyMaker
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlVideoFilesManager:

    @beartype
    def __init__(self, raw_data_path: str, video_path: str, video_files_metadata: list,
                    convert_timestamps: bool = True,
                    return_timestamps: bool = True):
        self.video_files_copy_maker = VideoFilesCopyMaker([video_files['name'] for video_files in video_files_metadata])
        self.video_files_copy_maker.copy(raw_data_path, video_path)
        self.fl_video_files_extractor = FlVideoFilesExtractor(raw_data_path, video_files_metadata,
                                                            convert_timestamps=convert_timestamps,
                                                            return_timestamps=return_timestamps)
        self.fl_video_files_builder = FlVideoFilesBuilder()

    def get_video_files(self):
        extracted_video_files = self.fl_video_files_extractor.extract_video_files()
        return [
            self.fl_video_files_builder.build(
                video_file["name"],
                video_file["timestamps"],
                video_file["device"]
            )
            for video_file in extracted_video_files
        ]
