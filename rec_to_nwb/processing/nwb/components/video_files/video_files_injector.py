class VideoFilesInjector:

    @staticmethod
    def inject(nwb_content, processing_module_name, image_series):
        nwb_content.processing[processing_module_name].add(image_series)
