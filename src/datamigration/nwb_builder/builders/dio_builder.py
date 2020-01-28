from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor


def build_dio(metadata, data_path, nwb_content):
    extracted_dio = DioExtractor(data_path=data_path,
                                 metadata=metadata)
    nwb_content.processing["behavior"].add_data_interface(
        extracted_dio.get_dio()
    )
