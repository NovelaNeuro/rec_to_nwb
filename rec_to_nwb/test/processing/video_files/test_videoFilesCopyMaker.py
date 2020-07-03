import os
from unittest import TestCase

from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.invalid_path_exception import InvalidPathException
from rec_to_nwb.processing.nwb.components.video_files.video_files_copy_maker import VideoFilesCopyMaker

path = os.path.dirname(os.path.abspath(__file__))


class TestVideoFilesCopyMaker(TestCase):

    def setUp(self):
        self.video_files_copy_maker = VideoFilesCopyMaker(['probe1.yml'])

    def test_copy_succes_valid_copied_to_destination(self):
        self.video_files_copy_maker.copy(path + "/../res", path + "/../res/video_test")
        self.assertTrue(os.path.isfile(path + '/../res/video_test/probe1.yml'))

    @should_raise(InvalidPathException)
    def test_copy_fail_invalid_destination_path(self):
        self.video_files_copy_maker.copy(path + "/../res", path + "/../res/wrong_path")

    def tearDown(self):
        if os.path.isfile(path + '/../res/video_test/probe1.yml'):
            os.remove(path + '/../res/video_test/probe1.yml')
