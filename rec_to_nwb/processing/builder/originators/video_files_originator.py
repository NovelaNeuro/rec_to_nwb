from rec_to_nwb.processing.nwb.components.video_files.fl_video_files_manager import FlVideoFilesManager
from rec_to_nwb.processing.nwb.components.video_files.video_files_creator import VideoFilesCreator
from rec_to_nwb.processing.nwb.components.video_files.video_files_injector import VideoFilesInjector


class VideoFilesOriginator:

    def __init__(self, datasets, video_directory, neb_content, processing_module_name):
        self.nwb_content = neb_content
        self.processing_module_name = processing_module_name
        self.video_directory = video_directory
        self.fl_video_files_manager = FlVideoFilesManager(datasets, video_directory)

    def make(self):
        fl_video_files = self.fl_video_files_manager.get_video_files()
        image_series = VideoFilesCreator.create(fl_video_files)
        VideoFilesInjector.inject(self.nwb_content, self.processing_module_name, image_series)