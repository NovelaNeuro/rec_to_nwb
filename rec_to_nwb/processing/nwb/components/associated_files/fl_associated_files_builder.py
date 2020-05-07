from rec_to_nwb.processing.nwb.components.associated_files.fl_associated_file import FlAssociatedFile


class FlAssociatedFilesBuilder:

    @staticmethod
    def build(name, description, content):
        return FlAssociatedFile(name, description, content)
