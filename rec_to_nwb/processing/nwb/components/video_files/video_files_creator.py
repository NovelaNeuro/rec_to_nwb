from ndx_franklab_novela.nwb_image_series import NwbImageSeries


class VideoFilesCreator:

    @staticmethod
    def create(fl_video_file, video_directory, nwb_content):
        return NwbImageSeries(
            devices=[nwb_content.devices['camera_device ' + str(fl_video_file.device)]],
            name=fl_video_file.name,
            timestamps=fl_video_file.timestamps,
            external_file=[video_directory + '/' + fl_video_file.name],
            format='external',
            starting_frame=[0],
            description='video of animal behavior from epoch'
        )
