from pynwb import NWBFile
from pynwb.behavior import BehavioralEvents

from rec_to_nwb.processing.tools.beartype.beartype import beartype


class VideoFilesInjector:

    @staticmethod
    @beartype
    def inject_all(nwb_content: NWBFile, image_series_list: list):
        video = BehavioralEvents(name='video')
        for image_series in image_series_list:
            VideoFilesInjector.__add_single_image_series(video, image_series)
        nwb_content.processing['behavior'].add(video)

    @staticmethod
    def __add_single_image_series(video, image_series):
        video.add_timeseries(image_series)
        return video
