from rec_to_nwb.processing.nwb.components.video_files.fl_video_files_manager import FlVideoFilesManager
from rec_to_nwb.processing.nwb.components.video_files.video_files_creator import VideoFilesCreator
from rec_to_nwb.processing.nwb.components.video_files.video_files_injector import VideoFilesInjector


class VideoFilesOriginator:

    def __init__(self, raw_data_path, video_path, video_files_metadata,
                    convert_timestamps=True,
                    return_timestamps=True):
        self.video_directory = video_path
        self.fl_video_files_manager = FlVideoFilesManager(raw_data_path, video_path, video_files_metadata,
                                                    convert_timestamps=convert_timestamps,
                                                    return_timestamps=return_timestamps)

    def make(self, nwb_content):
        fl_video_files = self.fl_video_files_manager.get_video_files()
        image_series_list = [
            VideoFilesCreator.create(fl_video_file, self.video_directory, nwb_content)
            for fl_video_file in fl_video_files
        ]
        VideoFilesInjector.inject_all(nwb_content, image_series_list)
