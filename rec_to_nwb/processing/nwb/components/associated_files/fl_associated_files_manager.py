from rec_to_nwb.processing.nwb.components.associated_files.fl_associated_files_builder import FlAssociatedFilesBuilder
from rec_to_nwb.processing.nwb.components.associated_files.fl_associated_files_reader import FlAssociatedFilesReader
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlAssociatedFilesManager:

    @beartype
    def __init__(self, associated_files_metadata: list):
        self.associated_files_metadata = associated_files_metadata
        self.fl_associated_files_reader = FlAssociatedFilesReader()
        self.fl_associated_files_builder = FlAssociatedFilesBuilder()

    def get_fl_associated_files(self):
        return [
            self.fl_associated_files_builder.build(
                file['name'],
                file['description'],
                self.fl_associated_files_reader.read(file["path"])
            )
            for file in self.associated_files_metadata
        ]

