from rec_to_nwb.processing.nwb.components.video_files.fl_video_files_manager import FlVideoFilesManager
from rec_to_nwb.processing.nwb.components.video_files.old_fl_video_files_manager import OldFlVideoFilesManager
from rec_to_nwb.processing.nwb.components.video_files.video_files_creator import VideoFilesCreator
from rec_to_nwb.processing.nwb.components.video_files.video_files_injector import VideoFilesInjector


class OldVideoFilesOriginator:

    def __init__(self, raw_data_path, video_path, video_files_metadata):
        self.video_directory = video_path
        self.old_fl_video_files_manager = OldFlVideoFilesManager(raw_data_path, video_path, video_files_metadata)

    def make(self, nwb_content):
        fl_video_files = self.old_fl_video_files_manager.get_video_files()
        image_series_list = [
            VideoFilesCreator.create(fl_video_file, self.video_directory, nwb_content)
            for fl_video_file in fl_video_files
        ]
        VideoFilesInjector.inject_all(nwb_content, image_series_list)
