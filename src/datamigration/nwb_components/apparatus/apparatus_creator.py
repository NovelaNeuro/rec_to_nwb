from src.datamigration.extension.apparatus import Apparatus


class ApparatusCreator:

    @staticmethod
    def create_apparatus(edges, nodes):
        return Apparatus(
            name='apparatus',
            edges=edges,
            nodes=nodes
        )