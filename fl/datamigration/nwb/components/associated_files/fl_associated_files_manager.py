from fl.datamigration.nwb.components.associated_files.fl_associated_file import FlAssociatedFile
from fl.datamigration.nwb.components.associated_files.fl_associated_files_builder import FlAssociatedFilesBuilder
from fl.datamigration.nwb.components.associated_files.fl_associated_files_extractor import FlAssociatedFilesExtractor


class FlAssociatedFilesManager:

    def __init__(self, files, files_metadata):
        self.fl_associated_files_extractor = FlAssociatedFilesExtractor(files)
        self.fl_associated_files_builder = FlAssociatedFilesBuilder()
        self.files_metadata = files_metadata

    def get_fl_associated_files(self):
        return [
            self.fl_associated_files_builder.build(
                file['name'],
                file['description'],
                self.fl_associated_files_extractor.extract()[i]
            ) for i, file in enumerate(self.files_metadata)]

