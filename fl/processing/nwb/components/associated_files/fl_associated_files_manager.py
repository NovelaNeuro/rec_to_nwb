from fldatamigration.processing.nwb.components.associated_files.fl_associated_files_builder import FlAssociatedFilesBuilder
from fldatamigration.processing.nwb.components.associated_files.fl_associated_files_extractor import FlAssociatedFilesExtractor
from fldatamigration.processing.tools.beartype.beartype import beartype


class FlAssociatedFilesManager:

    @beartype
    def __init__(self, files: list, files_metadata: list):
        self.files_metadata = files_metadata
        self.fl_associated_files_extractor = FlAssociatedFilesExtractor(files)
        self.fl_associated_files_builder = FlAssociatedFilesBuilder()

    def get_fl_associated_files(self):
        return [
            self.fl_associated_files_builder.build(
                file['name'],
                file['description'],
                self.fl_associated_files_extractor.extract()[i]
            )
            for i, file in enumerate(self.files_metadata)
        ]

