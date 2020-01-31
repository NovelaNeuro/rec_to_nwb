from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor


class DioBuilder:
    def __init__(self, metadata, data_path):
        self.metadata = metadata
        self.data_path = data_path

    def build(self):
        return DioExtractor(
            data_path=self.data_path,
            metadata=self.metadata
        ).get_dio()
