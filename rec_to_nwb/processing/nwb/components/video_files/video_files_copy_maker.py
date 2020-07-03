import os
from shutil import copy as copy_file

from rec_to_nwb.processing.exceptions.invalid_path_exception import InvalidPathException


class VideoFilesCopyMaker:

    def __init__(self, video_files_to_copy):
        self.video_files_to_copy = video_files_to_copy

    def copy(self, src, dst):
        if not os.path.exists(dst):
            raise InvalidPathException(dst + ' is not valid path')
        for video_file in self.video_files_to_copy:
            copy_file(src + '/' + video_file, dst)

