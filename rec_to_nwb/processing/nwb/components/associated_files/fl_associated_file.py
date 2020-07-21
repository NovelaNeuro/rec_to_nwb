from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlAssociatedFile:

    @beartype
    def __init__(self, name: str, description: str, content: str, task_epochs: str):
        self.name = name
        self.description = description
        self.content = content
        self.task_epochs = task_epochs
