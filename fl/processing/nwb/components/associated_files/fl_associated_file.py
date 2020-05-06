from fldatamigration.processing.tools.beartype.beartype import beartype


class FlAssociatedFile:

    @beartype
    def __init__(self, name: str, description: str, content: str):
        self.name = name
        self.description = description
        self.content = content
