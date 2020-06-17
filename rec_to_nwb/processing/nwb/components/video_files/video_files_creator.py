from ndx_franklab_novela.nwb_image_series import NwbImageSeries


class VideoFilesCreator:

    @staticmethod
    def create(fl_video_file):
        return NwbImageSeries(
            devices=fl_video_file.devices,
            name=fl_video_file.name,
            timestamps=fl_video_file.timestamps
        )
