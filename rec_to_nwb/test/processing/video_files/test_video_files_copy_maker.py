import os
from unittest import TestCase

from rec_to_nwb.processing.nwb.components.video_files.video_files_copy_maker import VideoFilesCopyMaker

path = os.path.dirname(os.path.abspath(__file__))


class TestVideoFilesCopyMaker(TestCase):

    def setUp(self):
        self.video_files_copy_maker = VideoFilesCopyMaker(['probe1.yml'])

    def test_copy_succes_valid_copied_to_destination(self):
        self.video_files_copy_maker.copy(path + "/../res", path + "/../res/video_test")
        self.assertTrue(os.path.isfile(path + '/../res/video_test/probe1.yml'))

    def tearDown(self):
        if os.path.isfile(path + '/../res/video_test/probe1.yml'):
            os.remove(path + '/../res/video_test/probe1.yml')




