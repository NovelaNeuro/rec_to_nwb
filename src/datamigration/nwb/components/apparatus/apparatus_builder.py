from src.datamigration.nwb.components.apparatus.lf_apparatus import LfApparatus


class ApparatusBuilder:

    @staticmethod
    def build(edges, nodes):
        return LfApparatus(edges, nodes)