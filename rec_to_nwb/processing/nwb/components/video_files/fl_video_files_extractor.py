import os


class FlVideoFilesExtractor:

    def __init__(self, datasets, video_directory):
        self.datasets = datasets
        self.video_directory = video_directory

    def extract_video_files(self):
        video_files = os.listdir(self.video_directory)
        extracted_video_files = []
        for video_file in video_files:
            new_fl_video_file = {}
            new_fl_video_file["name"] = str(video_file)
            new_fl_video_file["timestamps"] = 0
