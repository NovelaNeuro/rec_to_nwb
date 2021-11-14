from pathlib import Path

from rec_to_nwb.processing.header.xml_extractor import XMLExtractor


class HeaderFilesExtractor:

    def __init__(self):
        self.xml_files = []

    def extract_headers_from_rec_files(self, rec_files, copy_dir=None):
        for rec_file in rec_files:
            if copy_dir is not None:
                rec_copy = Path(copy_dir).joinpath(rec_file.name)
                xml_file = str(rec_copy) + '_header' + '.xml'
            else:
                xml_file = str(rec_file) + '_header' + '.xml'
            temp_xml_extractor = XMLExtractor(rec_path=rec_file,
                                              xml_path=xml_file)
            temp_xml_extractor.extract_xml_from_rec_file()
            self.xml_files.append(xml_file)
        return self.xml_files
