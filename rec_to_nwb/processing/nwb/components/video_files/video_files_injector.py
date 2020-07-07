from pynwb import NWBFile
from pynwb.behavior import BehavioralEvents

from rec_to_nwb.processing.tools.beartype.beartype import beartype


class VideoFilesInjector:

    @staticmethod
    @beartype
    def inject(nwb_content: NWBFile, image_series_list: list):
        video = BehavioralEvents(name='video')
        for image_series in image_series_list:
            video.add_timeseries(image_series)
        nwb_content.processing['behavior'].add(video)
