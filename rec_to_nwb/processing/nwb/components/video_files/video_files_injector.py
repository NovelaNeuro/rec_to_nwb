from pynwb import NWBFile
from pynwb.image import ImageSeries

from rec_to_nwb.processing.tools.beartype.beartype import beartype


class VideoFilesInjector:

    @beartype
    @staticmethod
    def inject(nwb_content: NWBFile, processing_module_name: str, image_series: ImageSeries):
        nwb_content.processing[processing_module_name].add(image_series)
