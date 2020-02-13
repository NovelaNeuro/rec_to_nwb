from src.datamigration.extension.apparatus import Apparatus


class ApparatusCreator:

    @classmethod
    def create_apparatus(cls,edges, nodes):
        return Apparatus(
            name='apparatus',
            edges=edges,
            nodes=nodes
        )