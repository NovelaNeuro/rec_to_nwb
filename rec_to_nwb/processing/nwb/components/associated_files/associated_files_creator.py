from ndx_franklab_novela import AssociatedFiles


class AssociatedFilesCreator:

    @classmethod
    def create(cls, fl_associated_file):
        return AssociatedFiles(
            name=fl_associated_file.name,
            description=fl_associated_file.description,
            content=fl_associated_file.content,
            task_epochs=fl_associated_file.task_epochs
        )
