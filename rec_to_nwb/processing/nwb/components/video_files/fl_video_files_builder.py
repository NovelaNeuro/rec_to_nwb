from rec_to_nwb.processing.nwb.components.video_files.fl_video_file import FlVideoFile


class FlVideoFilesBuilder:

    @staticmethod
    def build(name, timestamps, devices):
        return FlVideoFile(name, timestamps, devices)
