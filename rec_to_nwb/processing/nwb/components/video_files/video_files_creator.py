"""Creates a ImageSeries object that corresponds to the video"""
import os

from pynwb.image import ImageSeries


class VideoFilesCreator:

    @staticmethod
    def create(fl_video_file, video_directory, nwb_content):
        return ImageSeries(
            device=nwb_content.devices['camera_device ' +
                                       str(fl_video_file.device)],
            name=fl_video_file.name,
            timestamps=fl_video_file.timestamps,
            external_file=[os.path.join(video_directory, fl_video_file.name)],
            format='external',
            starting_frame=[0],
            description='video of animal behavior from epoch'
        )
