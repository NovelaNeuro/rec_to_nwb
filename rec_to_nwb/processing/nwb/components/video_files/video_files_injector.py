from pynwb import NWBFile
from pynwb.image import ImageSeries

from rec_to_nwb.processing.tools.beartype.beartype import beartype


class VideoFilesInjector:

    @staticmethod
    @beartype
    def inject(nwb_content: NWBFile, image_series: ImageSeries):
        nwb_content.add_stimulus(image_series)
