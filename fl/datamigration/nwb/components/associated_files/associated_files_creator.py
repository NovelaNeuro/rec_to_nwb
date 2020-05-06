from ndx_fl_novela.associated_files import AssociatedFiles


class AssociatedFilesCreator:

    @classmethod
    def create(cls, fl_associated_file):
        return AssociatedFiles(
                    name=fl_associated_file.name,
                    description=fl_associated_file.description,
                    content=fl_associated_file.content
            )

