from ndx_fllab_novela.apparatus import Apparatus


class ApparatusCreator:

    @classmethod
    def create_apparatus(cls, fl_apparatus):
        return Apparatus(
            name='apparatus',
            edges=fl_apparatus.edges,
            nodes=fl_apparatus.nodes
        )