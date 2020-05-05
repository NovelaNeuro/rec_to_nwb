from ndx_fl_novela.associated_files import AssociatedFiles


class AssociatedFilesCreator:

    def __init__(self, fl_associated_files):
        self.fl_associated_files = fl_associated_files

    def create(self):
        return [AssociatedFiles(
                    name=fl_associated_file.name,
                    description=fl_associated_file.description,
                    content=fl_associated_file.content
                ) for fl_associated_file in self.fl_associated_files]