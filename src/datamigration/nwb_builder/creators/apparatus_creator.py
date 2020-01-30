from src.datamigration.extension.apparatus import Apparatus


class ApparatusCreator:
    def create_apparatus(self, edges, nodes):
        return Apparatus(
            name='apparatus',
            edges=edges,
            nodes=nodes
        )