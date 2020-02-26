from ndx_franklab_novela.apparatus import Apparatus


class ApparatusCreator:

    @classmethod
    def create_apparatus(cls, lf_apparatus):
        return Apparatus(
            name='apparatus',
            edges=lf_apparatus.edges,
            nodes=lf_apparatus.nodes
        )