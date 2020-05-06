from fl.processing.header.header_checker.header_comparator import HeaderComparator
from fl.processing.header.header_checker.header_extractor import HeaderFilesExtractor
from fl.processing.header.header_checker.header_logger import HeaderLogger


class HeaderProcessor:

    @staticmethod
    def process_headers(rec_files_list):
        headers_extractor = HeaderFilesExtractor()
        header_files = headers_extractor.extract_headers_from_rec_files(rec_files_list)
        header_comparator = HeaderComparator(header_files)
        headers_differences = header_comparator.compare()

        HeaderLogger.log_header_differences(headers_differences, rec_files_list)

        return header_files[0]
