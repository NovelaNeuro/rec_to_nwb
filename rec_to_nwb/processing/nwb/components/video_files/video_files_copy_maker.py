from shutil import copy as copy_file


class VideoFilesCopyMaker:

    def __init__(self, video_files_to_copy):
        self.video_files_to_copy = video_files_to_copy

    def copy(self, src, dst):
        for video_file in self.video_files_to_copy:
            copy_file(src + '/' + video_file, dst)

